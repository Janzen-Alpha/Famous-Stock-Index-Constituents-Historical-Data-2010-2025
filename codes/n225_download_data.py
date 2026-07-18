"""
N225 Daily Closing Price Downloader
=====================================
根据 N225_constituents_by_year.csv 中各年度的成分股列表，
使用 yfinance 下载每只股票的后复权（Adj Close）日线收盘价，
按年份输出独立的 CSV 文件。

输出格式：
  - 第一行为股票代码（列标题）
  - 第一列为交易日期（索引）
  - 数据为后复权收盘价

用法：
  python download_n225_daily.py
"""

import yfinance as yf
import pandas as pd
import numpy as np
import os
import sys

# ============================================================
# 配置参数
# ============================================================
INPUT_FILE = 'N225_constituents_by_year.csv'   # 成分股列表
OUTPUT_DIR = 'n225_yearly_data'                 # 输出目录
YEARS = list(range(2010, 2026))                 # 2010 ~ 2025
START_DATE = '2010-01-01'
END_DATE = '2025-12-31'

# 批量下载大小（避免单次请求过多被限流，设为 0 表示一次性全部下载）
BATCH_SIZE = 0

# ============================================================
# 第1步：读取成分股数据
# ============================================================
print("=" * 60)
print("Step 1: 读取成分股列表...")

df_constituents = pd.read_csv(INPUT_FILE)
years_str = [str(y) for y in YEARS]

# 收集各年度股票代码
year_codes = {}
all_codes = set()

for year_str in years_str:
    codes = df_constituents[year_str].dropna().astype(str).str.strip().tolist()
    # 只保留纯数字代码（过滤可能的表头残留）
    codes = [c for c in codes if c.isdigit()]
    year_codes[year_str] = codes
    all_codes.update(codes)

print(f"年份范围: {min(YEARS)} - {max(YEARS)}")
print(f"去重后总股票数: {len(all_codes)}")

# 转换为 yfinance 格式（东京证券交易所后缀 .T）
all_tickers = sorted([f"{code}.T" for code in all_codes])
print(f"yfinance 代码示例: {all_tickers[:5]} ...")

# ============================================================
# 第2步：批量下载所有股票的日线数据
# ============================================================
print("\n" + "=" * 60)
print("Step 2: 下载后复权日线数据...")
print(f"共 {len(all_tickers)} 只股票，日期范围 {START_DATE} ~ {END_DATE}")
print("预计需要 2-5 分钟，请耐心等待...")

if BATCH_SIZE > 0:
    # 分批下载
    all_close_parts = []
    for i in range(0, len(all_tickers), BATCH_SIZE):
        batch = all_tickers[i:i + BATCH_SIZE]
        print(f"  正在下载第 {i // BATCH_SIZE + 1} 批 ({len(batch)} 只)...")
        data_batch = yf.download(
            batch,
            start=START_DATE, end=END_DATE,
            group_by='ticker', threads=True, auto_adjust=False,
            progress=False
        )
        close_batch = data_batch.xs('Adj Close', axis=1, level=1)
        all_close_parts.append(close_batch)

    close_prices = pd.concat(all_close_parts, axis=1)
else:
    # 一次性下载全部
    data = yf.download(
        all_tickers,
        start=START_DATE, end=END_DATE,
        group_by='ticker', threads=True, auto_adjust=False,
        progress=True
    )
    # 提取后复权收盘价（Adj Close）
    close_prices = data.xs('Adj Close', axis=1, level=1)

# 去掉列名中的 .T 后缀，恢复为纯数字代码
close_prices.columns = [col.replace('.T', '') for col in close_prices.columns]
close_prices.index.name = 'Date'

print(f"\n下载完成！数据形状: {close_prices.shape}")
print(f"日期范围: {close_prices.index[0].strftime('%Y-%m-%d')} ~ {close_prices.index[-1].strftime('%Y-%m-%d')}")
print(f"可用股票数: {len(close_prices.columns)}")

# ============================================================
# 第3步：按年度拆分并保存
# ============================================================
print("\n" + "=" * 60)
print("Step 3: 按年度拆分并保存 CSV...")

os.makedirs(OUTPUT_DIR, exist_ok=True)

summary_lines = []
total_missing = set()

for year_str in years_str:
    codes_this_year = year_codes[year_str]

    # 找到可用的列
    available = [c for c in codes_this_year if c in close_prices.columns]
    missing = set(codes_this_year) - set(available)
    total_missing.update(missing)

    # 截取该年数据
    year_start = f"{year_str}-01-01"
    year_end = f"{year_str}-12-31"
    year_data = close_prices.loc[year_start:year_end, available].copy()

    # 清洗1：去掉全年无数据的股票（如已退市、yfinance无数据）
    year_data = year_data.dropna(axis=1, how='all')
    # 清洗2：去掉所有股票都NaN的行（如日本市场休市日）
    year_data = year_data.dropna(axis=0, how='all')
    # 清洗3：前向+后向填充剩余NaN（处理年初休市日和零星缺失）
    year_data = year_data.ffill().bfill()
    # 清洗4：去掉填充后仍有NaN的列（真正有问题的股票，如全年无数据）
    year_data = year_data.dropna(axis=1, how='any')

    # 保存
    output_file = os.path.join(OUTPUT_DIR, f"N225_{year_str}.csv")
    year_data.to_csv(output_file, index=True)

    info = (
        f"{year_str}: {year_data.shape[1]} 只股票, "
        f"{year_data.shape[0]} 个交易日 -> {output_file}"
    )
    if missing:
        info += f"  [缺失: {', '.join(sorted(missing))}]"
    print(info)
    summary_lines.append(info)

# ============================================================
# 第4步：保存汇总
# ============================================================
print("\n" + "=" * 60)
print("Step 4: 保存汇总文件...")

summary_file = os.path.join(OUTPUT_DIR, 'summary.txt')
with open(summary_file, 'w', encoding='utf-8') as f:
    f.write("N225 Daily Closing Price Download Summary\n")
    f.write("=" * 50 + "\n")
    f.write(f"Date range: {START_DATE} to {END_DATE}\n")
    f.write(f"Total unique tickers attempted: {len(all_tickers)}\n")
    f.write(f"Total unique tickers with data: {len(close_prices.columns)}\n")
    if total_missing:
        f.write(f"Missing tickers (no data from yfinance): {sorted(total_missing)}\n")
    f.write("\n--- Per Year ---\n")
    for line in summary_lines:
        f.write(line + "\n")

print(f"汇总已保存至: {summary_file}")
print("\n" + "=" * 60)
print("全部完成！")
print(f"输出目录: {os.path.abspath(OUTPUT_DIR)}/")
print(f"文件列表: {', '.join(sorted(os.listdir(OUTPUT_DIR)))}")
