"""
CSI 300 历史日线数据下载
使用 westockdata CLI (后复权) 
每个年份一个 CSV: 第一行=股票代码, 第一列=日期
"""
import pandas as pd
import subprocess
import re
import os
import time
import sys

# ============================================================
# 1. 读取成分股
# ============================================================
raw_df = pd.read_csv('data/csi300/CSI300_constituents_by_year_raw.csv')
yearly_stocks = {}
all_stocks = set()

for year in range(2010, 2026):
    row = raw_df[raw_df['year'] == year].iloc[0, 1:]
    stocks = [s for s in row.dropna().tolist() if s]
    yearly_stocks[year] = stocks
    all_stocks.update(stocks)

print(f"年份: {len(yearly_stocks)}, 唯一股票: {len(all_stocks)}")

# Convert to CLI format: SH600519 -> sh600519, SZ000858 -> sz000858
def to_cli(code):
    return code.lower()

# Convert back to yfinance format
def to_yf(code):
    if code.startswith('SH'):
        return code[2:] + '.SS'
    elif code.startswith('SZ'):
        return code[2:] + '.SZ'
    return code

# ============================================================
# 2. 批量下载
# ============================================================
all_stocks_list = sorted(all_stocks)
BATCH_SIZE = 50
LIMIT = 4000  # covers 2010-2026 (~3900 trading days)
MAX_RETRIES = 2

# Create output directory
os.makedirs('data/csi300/daily', exist_ok=True)

# Storage: {code: DataFrame with date index and 'close' column}
price_data = {}

# Process in batches
total_batches = (len(all_stocks_list) + BATCH_SIZE - 1) // BATCH_SIZE

for batch_idx in range(0, len(all_stocks_list), BATCH_SIZE):
    batch = all_stocks_list[batch_idx:batch_idx + BATCH_SIZE]
    batch_num = batch_idx // BATCH_SIZE + 1
    cli_codes = ','.join(to_cli(c) for c in batch)
    
    print(f"\n批次 {batch_num}/{total_batches}: {len(batch)} stocks...", flush=True)
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            cmd = f'npx -y westock-data-clawhub@1.0.4 kline {cli_codes} --period day --limit {LIMIT} --fq hfq'
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, 
                timeout=120, encoding='utf-8'
            )
            output = result.stdout
            
            if 'error' in output.lower() and 'retry' in output.lower():
                print(f"  重试 {attempt+1}...", flush=True)
                time.sleep(3)
                continue
            
            # Parse markdown table
            lines = output.strip().split('\n')
            rows = []
            for line in lines:
                # Match table rows: | symbol | date | open | last | ...
                match = re.match(r'\|\s*(\w+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|.*?\|\s*([\d.]+)\s*\|', line)
                if match:
                    symbol = match.group(1).upper()  # sh600519 -> SH600519
                    date = match.group(2)
                    close = float(match.group(3))
                    rows.append({'code': symbol, 'date': date, 'close': close})
            
            if rows:
                df = pd.DataFrame(rows)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                # Store by stock
                for code in df['code'].unique():
                    sub = df[df['code'] == code].set_index('date')['close']
                    if code not in price_data or len(sub) > len(price_data[code]):
                        price_data[code] = sub
                
                print(f"  ✓ 获取 {len(rows)} 条数据 ({df['date'].min().date()} ~ {df['date'].max().date()})", flush=True)
                break
            else:
                print(f"  ⚠ 未解析到数据", flush=True)
                break
                
        except subprocess.TimeoutExpired:
            print(f"  超时, 重试 {attempt+1}...", flush=True)
            time.sleep(5)
        except Exception as e:
            print(f"  错误: {e}", flush=True)
            time.sleep(3)
    
    # Rate limiting
    time.sleep(1)

print(f"\n下载完成: {len(price_data)}/{len(all_stocks)} stocks")

# ============================================================
# 3. 按年份输出 CSV
# ============================================================
print("\n生成年度CSVs...")

for year in range(2010, 2026):
    stocks = yearly_stocks[year]
    date_range = pd.date_range(f'{year}-01-01', f'{year}-12-31', freq='B')  # business days
    
    # Build DataFrame: columns = stock yfinance codes, index = dates, values = close
    col_data = {}
    available = 0
    for code in stocks:
        yf_code = to_yf(code)
        if code in price_data:
            series = price_data[code]
            # Filter to this year
            series_year = series[(series.index >= f'{year}-01-01') & (series.index <= f'{year}-12-31')]
            if len(series_year) > 0:
                col_data[yf_code] = series_year
                available += 1
    
    if col_data:
        df = pd.DataFrame(col_data)
        df.index.name = 'date'
        df = df.sort_index()
        
        output = f'data/csi300/daily/CSI300_{year}_daily.csv'
        df.round(4).to_csv(output)
        print(f"  {year}: {available}/{len(stocks)} stocks, {len(df)} days -> {output}")
    else:
        print(f"  {year}: 0 stocks available")

print("\n完成!")
