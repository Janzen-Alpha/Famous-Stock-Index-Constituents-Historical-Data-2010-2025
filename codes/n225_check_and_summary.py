"""
Final Check & Summary Generator
================================
1. 逐年度检查缺失值 → NaN >3 则删除
2. 确保同一年度所有股票行数一致
3. 生成 N225_constituents_summary.csv：每年实际包含完整数据的股票列表

输出：
  - N225_constituents_summary.csv
"""

import pandas as pd
import os
import glob

DATA_DIR = 'n225_yearly_data'
OUTPUT_FILE = os.path.join(DATA_DIR, 'N225_constituents_summary.csv')

print("=" * 60)
print("最终数据检查与汇总")
print("=" * 60)

files = sorted(glob.glob(os.path.join(DATA_DIR, 'N225_constituents_close_*.csv')))

summary_data = {}  # year -> set of stock codes
all_years = []
removed_any = False

for f in files:
    year = os.path.basename(f).replace('N225_constituents_close_', '').replace('.csv', '')
    all_years.append(year)
    df = pd.read_csv(f, index_col=0)

    initial_count = df.shape[1]
    removed = []

    # --- 检查1：NaN 数量 ---
    nan_counts = df.isna().sum()
    for col in df.columns:
        if nan_counts[col] > 3:
            removed.append(f"{col}(NaN={nan_counts[col]})")
            df.drop(columns=[col], inplace=True)

    # --- 检查2：行数一致性 ---
    if df.shape[1] > 0:
        row_counts = df.notna().sum()
        expected = row_counts.median()
        for col in list(df.columns):
            if row_counts[col] != expected:
                removed.append(f"{col}(rows={row_counts[col]} vs {expected})")
                df.drop(columns=[col], inplace=True)

    # --- 保存 ---
    if removed:
        removed_any = True
        df.to_csv(f, index=True)
        print(f"  {year}: 删除 {len(removed)} 只: {', '.join(removed)}")
        print(f"     {initial_count} -> {df.shape[1]} stocks")

    # 收集完整数据的股票列表
    summary_data[year] = set(df.columns)

    nan_final = df.isna().sum().sum()
    consistent = df.notna().sum().nunique() == 1 if df.shape[1] > 0 else True

    status = "OK" if (nan_final == 0 and consistent) else f"NaN={nan_final}, consistent={consistent}"
    print(f"  {year}: {df.shape[1]} stocks x {df.shape[0]} days [{status}]")

# ============================================================
# 生成汇总 CSV
# ============================================================
print(f"\n生成汇总文件: {OUTPUT_FILE}")

# 收集所有出现过的股票代码
all_codes = set()
for codes in summary_data.values():
    all_codes.update(codes)
all_codes = sorted(all_codes)

# 构建 DataFrame: 行=股票代码, 列=年份, 值=1(有数据)/0(无)
summary_df = pd.DataFrame(index=all_codes, columns=all_years, dtype=int)
summary_df = summary_df.fillna(0)

for year, codes in summary_data.items():
    for code in codes:
        summary_df.loc[code, year] = 1

# 添加统计列
summary_df['total_years'] = summary_df.sum(axis=1)
summary_df = summary_df.sort_values('total_years', ascending=False)

summary_df.to_csv(OUTPUT_FILE)
print(f"  共 {len(all_codes)} 只独特股票")
print(f"  全16年均有数据的股票: {(summary_df['total_years'] == 16).sum()} 只")
print(f"  各年股票数: {[(y, len(summary_data[y])) for y in all_years]}")

print("\n全部完成！")
