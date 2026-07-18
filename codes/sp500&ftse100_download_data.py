"""
============================================================================
  历史日线数据下载程序 - S&P 500 & FTSE 100 (2010-2025)
  功能: 根据成分股列表，从 yfinance 批量下载后除权日线收盘价
  输出: 每年一个 CSV，第一行=股票代码，第一列=日期，数据=Adj Close
============================================================================
使用方法:
  1. 确保 SP500_Yearly_LastTradingDay.csv 和 FTSE100_yearly_2010to2025_final.csv 在同目录
  2. 运行: python download_data.py
  3. 输出: sp500_daily/ 和 ftse100_daily/ 文件夹，各含16个年度CSV
============================================================================
"""
import yfinance as yf
import pandas as pd
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
START = '2010-01-01'
END = '2025-12-31'


def read_constituents(filepath, year_range):
    """读取转置格式的成分股CSV: 第1行=年份, 每列=股票代码"""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        years = next(reader)
        columns = {y: [] for y in years}
        for row in reader:
            for i, ticker in enumerate(row):
                t = ticker.strip()
                if t:
                    columns[years[i]].append(t)
    return {y: columns[y] for y in columns if y in year_range}


def fix_sp500_ticker(t):
    """SP500: 将 BRK.B 转为 BRK-B (yfinance 格式)"""
    return t.replace('.', '-')


def download_batch(tickers, name):
    """批量下载所有 ticker 的历史数据"""
    tickers = sorted(tickers)
    print(f"\n[{name}] 正在下载 {len(tickers)} 只股票...")
    data = yf.download(
        tickers, start=START, end=END,
        auto_adjust=False, threads=True, progress=False
    )
    adj = data['Adj Close']  # 后除权收盘价
    print(f"  下载完成: {adj.shape[0]} 天 x {adj.shape[1]} 只")
    return adj


def save_yearly(full_data, constituents, index_name, out_subdir):
    """按年份拆分并保存"""
    out_dir = os.path.join(BASE_DIR, out_subdir)
    os.makedirs(out_dir, exist_ok=True)

    for year_str in sorted(constituents.keys()):
        year = int(year_str)
        raw_tickers = constituents[year_str]

        # 转换 ticker 格式匹配 yfinance 输出
        if index_name == 'SP500':
            year_tickers = [fix_sp500_ticker(t) for t in raw_tickers]
        else:
            year_tickers = raw_tickers

        available = [t for t in year_tickers if t in full_data.columns]
        missing = [t for t in year_tickers if t not in full_data.columns]

        year_data = full_data.loc[f'{year}-01-01':f'{year}-12-31', available].copy()
        year_data = year_data.dropna(how='all')

        csv_path = os.path.join(out_dir, f'{index_name}_{year}.csv')
        year_data.to_csv(csv_path, index_label='Date')

        print(f"  {year}: {len(available)}/{len(year_tickers)} tickers, "
              f"{len(year_data)} 天 → {os.path.basename(csv_path)}")
        if missing:
            print(f"         缺失({len(missing)}): {sorted(missing)[:5]}...")


# ================================================================
# 主程序
# ================================================================
yr_set = {str(y) for y in range(2010, 2026)}

# --- 读取成分股 ---
sp500 = read_constituents(
    os.path.join(BASE_DIR, "SP500_Yearly_LastTradingDay.csv"), yr_set)
ftse = read_constituents(
    os.path.join(BASE_DIR, "FTSE100_yearly_2010to2025_final.csv"), yr_set)

# --- 收集所有唯一 ticker ---
all_sp500 = set()
for ts in sp500.values():
    for t in ts:
        all_sp500.add(fix_sp500_ticker(t))

all_ftse = set()
for ts in ftse.values():
    all_ftse.update(ts)

print(f"SP500: {len(all_sp500)} unique tickers")
print(f"FTSE100: {len(all_ftse)} unique tickers")

# --- 批量下载 ---
sp500_data = download_batch(all_sp500, "SP500")
ftse_data = download_batch(all_ftse, "FTSE100")

# --- 按年保存 ---
print("\n" + "=" * 60)
print("保存 S&P 500 年度数据 → sp500_daily/")
print("=" * 60)
save_yearly(sp500_data, sp500, 'SP500', 'sp500_daily')

print("\n" + "=" * 60)
print("保存 FTSE 100 年度数据 → ftse100_daily/")
print("=" * 60)
save_yearly(ftse_data, ftse, 'FTSE100', 'ftse100_daily')

print("\n完成!")
