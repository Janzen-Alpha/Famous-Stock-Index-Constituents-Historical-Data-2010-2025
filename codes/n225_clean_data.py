"""
N225 Daily Data Cleaner & Renamer
===================================
从原始 yfinance 数据重新处理：
1. 去除休市日（全NaN行）
2. 检测连续NaN > 3天 → 删除该股票（该年度内）
3. 1-2天NaN → ffill 前向填充
4. 检测连续相同值 > 3天（非停牌原因）→ 删除
5. 重命名为 N225_constituents_close_年份.csv

用法：
  python clean_n225_daily.py
"""

import yfinance as yf
import pandas as pd
import numpy as np
import os
import glob

# ============================================================
# 配置
# ============================================================
INPUT_FILE = 'N225_constituents_by_year.csv'
OUTPUT_DIR = 'n225_yearly_data'
YEARS = list(range(2010, 2026))
START_DATE = '2010-01-01'
END_DATE = '2025-12-31'
MAX_NAN_CONSEC = 3       # 连续NaN超过此天数 → 删除
MAX_FLAT_CONSEC = 10     # 连续相同价格超过此天数 → 删除（提高阈值避免金周误判）
NAN_ROW_THRESHOLD = 0.8  # 某行超过此比例的股票为NaN → 视为休市日删除

# ============================================================
# 第1步：读取成分股 & 下载原始数据
# ============================================================
print("=" * 60)
print("Step 1: 读取成分股 & 下载原始数据...")

df_constituents = pd.read_csv(INPUT_FILE)
years_str = [str(y) for y in YEARS]

year_codes = {}
all_codes = set()
for ys in years_str:
    codes = df_constituents[ys].dropna().astype(str).str.strip().tolist()
    codes = [c for c in codes if c.isdigit()]
    year_codes[ys] = codes
    all_codes.update(codes)

all_tickers = sorted([f"{code}.T" for code in all_codes])
print(f"总计 {len(all_codes)} 只去重股票，{len(all_tickers)} 个 ticker")

data = yf.download(
    all_tickers, start=START_DATE, end=END_DATE,
    group_by='ticker', threads=True, auto_adjust=False, progress=True
)
raw_close = data.xs('Adj Close', axis=1, level=1)
raw_close.columns = [col.replace('.T', '') for col in raw_close.columns]
raw_close.index.name = 'Date'

print(f"原始数据形状: {raw_close.shape}")
print(f"日期范围: {raw_close.index[0]} ~ {raw_close.index[-1]}")

# ============================================================
# 第2步：逐年度清洗
# ============================================================
print("\n" + "=" * 60)
print("Step 2: 逐年度清洗数据...")

# 注意：新旧文件命名不同（N225_constituents_close_YYYY vs N225_YYYY），不会冲突
# 旧文件 N225_YYYY.csv 可在确认新数据无误后手动删除

report_lines = []
total_removed_nan = 0
total_removed_flat = 0

for ys in years_str:
    codes_this_year = year_codes[ys]
    available = [c for c in codes_this_year if c in raw_close.columns]
    missing_codes = set(codes_this_year) - set(available)

    # 截取该年数据
    year_start = f"{ys}-01-01"
    year_end = f"{ys}-12-31"
    year_data = raw_close.loc[year_start:year_end, available].copy()

    initial_cols = year_data.shape[1]

    # --- 清洗1: 去掉全年无数据的股票 ---
    year_data = year_data.dropna(axis=1, how='all')

    # --- 清洗2: 去掉休市日（>80%股票为NaN的行） ---
    nan_ratio = year_data.isna().sum(axis=1) / year_data.shape[1]
    year_data = year_data.loc[nan_ratio <= (1 - NAN_ROW_THRESHOLD)]

    # --- 清洗3: 检测并删除有连续NaN > MAX_NAN_CONSEC天的股票 ---
    removed_nan = []
    for col in list(year_data.columns):
        s = year_data[col]
        # 找出所有NaN的位置
        nan_mask = s.isna()
        if not nan_mask.any():
            continue
        # 计算连续NaN组
        grp = (nan_mask != nan_mask.shift()).cumsum()
        nan_groups = grp[nan_mask]
        max_consec_nan = nan_groups.value_counts().max() if len(nan_groups) > 0 else 0
        if max_consec_nan > MAX_NAN_CONSEC:
            removed_nan.append((col, max_consec_nan))
            year_data.drop(columns=[col], inplace=True)

    # --- 清洗4: 1-2天NaN → ffill填充 ---
    year_data = year_data.ffill()

    # --- 清洗5: 填充后仍有NaN的列 → 删除 ---
    year_data = year_data.dropna(axis=1, how='any')

    # --- 清洗6: 检测连续相同值 > MAX_FLAT_CONSEC天 ---
    removed_flat = []
    for col in list(year_data.columns):
        s = year_data[col]
        # 找出连续相同值的组
        grp = (s != s.shift()).cumsum()
        max_consec = grp.value_counts().max()
        if max_consec > MAX_FLAT_CONSEC:
            # 找到最长的那段
            max_grp_id = grp.value_counts().idxmax()
            streak_start = grp[grp == max_grp_id].index[0]
            streak_end = grp[grp == max_grp_id].index[-1]
            removed_flat.append((col, max_consec, str(streak_start), str(streak_end)))
            year_data.drop(columns=[col], inplace=True)

    # --- 保存 ---
    output_file = os.path.join(OUTPUT_DIR, f"N225_constituents_close_{ys}.csv")
    year_data.to_csv(output_file, index=True)

    final_cols = year_data.shape[1]
    n_removed = initial_cols - final_cols
    total_removed_nan += len(removed_nan)
    total_removed_flat += len(removed_flat)

    report = (
        f"{ys}: {initial_cols} → {final_cols} stocks "
        f"(-{n_removed}), {year_data.shape[0]} trading days"
    )
    if missing_codes:
        report += f"  [yfinance缺失: {sorted(missing_codes)}]"
    print(report)
    report_lines.append(report)

    if removed_nan:
        for code, cons in removed_nan:
            print(f"  NaN删除: {code} (最长连续NaN {cons}天)")
    if removed_flat:
        for code, cons, start, end in removed_flat:
            print(f"  平值删除: {code} ({cons}天相同, {start}~{end})")

# ============================================================
# 第3步：保存报告
# ============================================================
print("\n" + "=" * 60)
print("Step 3: 保存清洗报告...")

report_file = os.path.join(OUTPUT_DIR, 'cleaning_report.txt')
with open(report_file, 'w', encoding='utf-8') as f:
    f.write("N225 Data Cleaning Report\n")
    f.write("=" * 50 + "\n")
    f.write(f"Continuous NaN threshold: > {MAX_NAN_CONSEC} days → remove\n")
    f.write(f"Continuous flat threshold: > {MAX_FLAT_CONSEC} days → remove\n")
    f.write(f"Holiday row threshold: > {NAN_ROW_THRESHOLD*100:.0f}% NaN → drop row\n")
    f.write(f"NaN gaps ≤ {MAX_NAN_CONSEC} days → forward fill\n")
    f.write(f"\nTotal stocks removed for NaN: {total_removed_nan}\n")
    f.write(f"Total stocks removed for flat: {total_removed_flat}\n")
    f.write("\n--- Per Year Summary ---\n")
    for line in report_lines:
        f.write(line + "\n")

print(f"报告已保存: {report_file}")

# 列出最终文件
print("\n最终输出文件:")
for f in sorted(glob.glob(os.path.join(OUTPUT_DIR, 'N225_constituents_close_*.csv'))):
    df = pd.read_csv(f, index_col=0)
    year = os.path.basename(f).replace('N225_constituents_close_', '').replace('.csv', '')
    print(f"  N225_constituents_close_{year}.csv: {df.shape[1]} stocks × {df.shape[0]} days")

print("\n全部完成！")
