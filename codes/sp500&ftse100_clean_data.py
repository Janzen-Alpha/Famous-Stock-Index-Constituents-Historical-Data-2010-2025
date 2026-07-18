"""
============================================================================
  数据清洗与验证程序
  功能:
    1. 检查每个年度 CSV 的缺失值
    2. 缺失值超过 3 个的股票列直接删除
    3. 先清除市场休市日（所有股票同时缺失的行），再统计单股缺失
    4. 确保同一年度所有股票交易日数一致，无任何 NaN
============================================================================
使用方法:
  python clean_data.py
  输入: sp500_daily/ 和 ftse100_daily/ 下的年度 CSV
  输出:
    - sp500_daily_cleaned/  清洗后数据
    - ftse100_daily_cleaned/ 清洗后数据
    - SP500_valid_tickers_yearly.csv  有效股票列表（转置格式）
    - FTSE100_valid_tickers_yearly.csv
============================================================================
"""
import pandas as pd
import os
import csv

BASE = os.path.dirname(os.path.abspath(__file__))

for index_name, subdir in [("SP500", "sp500_daily"), ("FTSE100", "ftse100_daily")]:
    in_dir = os.path.join(BASE, subdir)
    out_dir = os.path.join(BASE, f"{subdir}_cleaned")
    os.makedirs(out_dir, exist_ok=True)

    print("=" * 70)
    print(f"  处理 {index_name}")
    print("=" * 70)

    files = sorted([f for f in os.listdir(in_dir) if f.endswith('.csv')])
    all_yearly_valid = {}
    total_before, total_after = 0, 0

    for fname in files:
        year = fname.replace(f'{index_name}_', '').replace('.csv', '')
        fpath = os.path.join(in_dir, fname)
        df = pd.read_csv(fpath, index_col=0, parse_dates=True)
        tickers_before = len(df.columns)

        # Step 1: 删除整行缺失的行（市场休市日）
        df = df.dropna(axis=0, how='all')

        # Step 2: 删除大部分股票都缺失的行（异常交易日）
        threshold = max(0.8, 1.0 - 5.0 / len(df.columns))
        bad_rows = df.isnull().mean(axis=1) > threshold
        df = df[~bad_rows]

        # Step 3: 统计每列的真正缺失值
        nan_counts = df.isnull().sum()
        max_rows = len(df)

        # Step 4: 缺失 > 3 的列删除
        to_drop = nan_counts[nan_counts > 3].index.tolist()
        to_keep = nan_counts[nan_counts <= 3].index.tolist()

        if to_drop:
            df = df.drop(columns=to_drop)

        # Step 5: 删除仍有 NaN 的行
        df = df.dropna(axis=0, how='any')

        tickers_after = len(df.columns)
        total_before += tickers_before
        total_after += tickers_after

        # 报告
        print(f"\n{year}: {tickers_before} → {tickers_after} tickers, {len(df)} 天, {df.isnull().sum().sum()} NaN")

        if to_drop:
            dropped_counts = nan_counts[to_drop]
            all_missing = dropped_counts[dropped_counts == max_rows]
            partial = dropped_counts[(dropped_counts > 3) & (dropped_counts < max_rows)]
            if len(all_missing) > 0:
                print(f"  无数据({len(all_missing)}只): {', '.join(all_missing.index[:10])}{'...' if len(all_missing) > 10 else ''}")
            if len(partial) > 0:
                for t in partial.index:
                    print(f"  缺口过多: {t} ({int(partial[t])} NaN)")
        else:
            print(f"  完美!")

        # 保存
        out_path = os.path.join(out_dir, fname)
        df.to_csv(out_path, index_label='Date')
        all_yearly_valid[year] = to_keep

    # 输出年度有效股票列表（转置格式）
    summary_path = os.path.join(BASE, f'{index_name}_valid_tickers_yearly.csv')
    years = sorted(all_yearly_valid.keys())
    max_len = max(len(v) for v in all_yearly_valid.values())

    with open(summary_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(years)
        for i in range(max_len):
            row = []
            for y in years:
                tickers = all_yearly_valid[y]
                row.append(tickers[i] if i < len(tickers) else '')
            writer.writerow(row)

    kept_pct = total_after / total_before * 100 if total_before > 0 else 0
    print(f"\n总计: {total_before} → {total_after} (保留 {kept_pct:.0f}%)")
    print(f"清洗后数据: {out_dir}/")
    print(f"有效股票列表: {summary_path}")
    print()

print("全部完成!")
