"""
数据清洗与验证程序
- 检查每个年度CSV的缺失值
- 缺失值超过3个的股票列直接删除
- 确保同一年度所有股票的数据行数一致
- 输出清洗后的CSV + 有效股票列表
"""
import pandas as pd
import os
import csv

BASE = r"D:\agent\agent_academic\韩国股市对比小论文\6 获取中美英日韩数据\data\sp500"

for index_name, subdir in [("SP500", "sp500_daily"), ("FTSE100", "ftse100_daily")]:
    in_dir = os.path.join(BASE, subdir)
    out_dir = os.path.join(BASE, f"{subdir}_cleaned")
    list_dir = os.path.join(BASE, f"{subdir}_tickers")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(list_dir, exist_ok=True)
    
    print("=" * 70)
    print(f"PROCESSING {index_name}")
    print("=" * 70)
    
    # Collect files sorted by year
    files = sorted([f for f in os.listdir(in_dir) if f.endswith('.csv')])
    
    all_yearly_valid = {}
    total_before, total_after = 0, 0
    
    for fname in files:
        year = fname.replace(f'{index_name}_', '').replace('.csv', '')
        fpath = os.path.join(in_dir, fname)
        
        df = pd.read_csv(fpath, index_col=0, parse_dates=True)
        tickers_before = len(df.columns)
        
        # Step 1: 先删除整行缺失的行（市场休市日，如节假日）
        # 这些行对所有股票都缺失，不应影响单只股票的缺失统计
        df = df.dropna(axis=0, how='all')
        
        # Step 2: 删除大部分股票都缺失的行（如整个市场某日无交易的比例 > 80%）
        threshold_pct = max(0.8, 1.0 - 5.0 / len(df.columns))
        rows_to_drop = df.isnull().mean(axis=1) > threshold_pct
        df = df[~rows_to_drop]
        
        # Step 3: 现在统计每列的真实缺失值
        nan_counts = df.isnull().sum()
        max_rows = len(df)
        
        # 标记删除：缺失值 > 3
        to_drop = nan_counts[nan_counts > 3].index.tolist()
        to_keep = nan_counts[nan_counts <= 3].index.tolist()
        
        if to_drop:
            df = df.drop(columns=to_drop)
        
        # Step 4: 删除仍有缺失值的行（确保所有股票在同一交易日有数据）
        df = df.dropna(axis=0, how='any')
        
        data_rows = len(df)
        tickers_after = len(df.columns)
        
        total_before += tickers_before
        total_after += tickers_after
        
        # 详细报告
        print(f"\n{year}: {tickers_before} → {tickers_after} tickers, {data_rows} days")
        
        if to_drop:
            # 分类：>3缺失 vs 全年缺失 vs 少量缺失
            dropped_counts = nan_counts[to_drop]
            all_missing = dropped_counts[dropped_counts == max_rows]  # 全年缺失
            partial_missing = dropped_counts[(dropped_counts > 3) & (dropped_counts < max_rows)]
            
            if len(all_missing) > 0:
                print(f"  全年无数据({len(all_missing)}): {', '.join(all_missing.index)}")
            if len(partial_missing) > 0:
                for t in partial_missing.index:
                    print(f"  缺口过多: {t} ({int(partial_missing[t])} NaN)")
        else:
            print(f"  完美: 所有{tickers_after}只股票数据完整")
        
        # 保存清洗后数据
        out_path = os.path.join(out_dir, fname)
        df.to_csv(out_path, index_label='Date')
        
        # 保存有效股票列表
        all_yearly_valid[year] = to_keep
        
        list_path = os.path.join(list_dir, f'{index_name}_{year}_tickers.csv')
        with open(list_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ticker'])
            for t in to_keep:
                writer.writerow([t])
    
    # 输出汇总的年度有效股票列表（转置格式）
    summary_path = os.path.join(BASE, f'{index_name}_valid_tickers_yearly.csv')
    years = sorted(all_yearly_valid.keys())
    max_len = max(len(v) for v in all_yearly_valid.values())
    
    with open(summary_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(years)
        for i in range(max_len):
            row = [all_yearly_valid[y][i] if i < len(all_yearly_valid[y]) else '' for y in years]
            writer.writerow(row)
    
    print(f"\n{'='*50}")
    print(f"{index_name} SUMMARY: {total_before} → {total_after} total ticker-year entries")
    print(f"  Cleaned CSVs: {out_dir}/")
    print(f"  Ticker lists: {list_dir}/")
    print(f"  Yearly summary: {summary_path}")
    print()

print("All done!")
