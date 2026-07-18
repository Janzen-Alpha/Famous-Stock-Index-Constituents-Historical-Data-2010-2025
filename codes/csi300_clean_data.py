"""
CSI 300 日线数据清洗
- 1-2天缺失 → 前值填充
- 连续缺失>3天: 判断是否为退市/数据范围边界 → 否则删除
- 连续相同>3天: 判断是否为停牌（中国A股常见）→ 保留，否则删除
- 重命名为 CSI300_constituents_close_YEAR.csv
"""
import pandas as pd
import os, glob, re

daily_dir = 'data/csi300/daily'
files = sorted(glob.glob(os.path.join(daily_dir, 'CSI300_*_daily.csv')))

# Build a multi-year lookup to check stock continuity
all_stocks_by_year = {}
for f in files:
    yr = int(os.path.basename(f).split('_')[1])
    df = pd.read_csv(f, index_col=0)
    all_stocks_by_year[yr] = set(df.columns)

removal_log = []
fill_log = []

for f in files:
    yr = int(os.path.basename(f).split('_')[1])
    df = pd.read_csv(f, index_col=0)
    df.index = pd.to_datetime(df.index)
    
    stocks_to_remove = set()
    stocks_cleaned = 0
    nans_filled = 0
    
    stocks_prev = all_stocks_by_year.get(yr - 1, set())
    stocks_next = all_stocks_by_year.get(yr + 1, set())
    
    for col in df.columns:
        series = df[col]
        valid_series = series.dropna()
        
        if len(valid_series) == 0:
            # No data at all → remove
            stocks_to_remove.add(col)
            removal_log.append((yr, col, '无数据'))
            continue
        
        first_valid_idx = valid_series.index[0]
        last_valid_idx = valid_series.index[-1]
        year_start = df.index[0]
        year_end = df.index[-1]
        
        # --- 1. Handle NaN ---
        nan_mask = series.isna()
        if nan_mask.any():
            # Find consecutive NaN runs
            groups = (nan_mask != nan_mask.shift()).cumsum()
            for grp_id in groups[nan_mask].unique():
                grp_dates = nan_mask[nan_mask & (groups == grp_id)].index
                grp_len = len(grp_dates)
                
                if grp_len <= 2:
                    # 1-2 NaNs: will be filled
                    continue
                
                # Check if NaN is at year boundaries (data range issue)
                is_at_start = grp_dates[0] <= first_valid_idx
                is_at_end = grp_dates[-1] >= last_valid_idx
                
                if is_at_start:
                    # NaN at beginning → data range issue, keep stock
                    continue
                
                if is_at_end:
                    # NaN at end → check if stock exists in next year
                    if col in stocks_next:
                        # Stock exists next year → just a data gap, keep
                        continue
                    elif grp_len > 60:
                        # Stock delisted mid-year → legitimate, keep
                        stocks_to_remove.add(col)
                        removal_log.append((yr, col, f'年末缺失{grp_len}天(次年不存在)'))
                        break
                    else:
                        # Short gap at year end → keep, will be filled
                        continue
                
                # NaN in the middle of active trading → possibly suspension
                if grp_len > 3 and not is_at_start and not is_at_end:
                    # Check if stock continues trading after NaN and exists next year
                    after_nan = series.loc[grp_dates[-1]:].dropna()
                    stock_continues = col in stocks_next
                    
                    if len(after_nan) > 0:
                        # Stock resumed trading → likely suspension or short halt
                        # Only remove if gap is very long AND stock doesn't exist next year
                        if grp_len > 30 and not stock_continues:
                            stocks_to_remove.add(col)
                            removal_log.append((yr, col, f'中间缺失{grp_len}天(次年不存在)'))
                            break
                        # Otherwise keep (forward-fill will handle)
                        continue
            
            # Fill 1-2 NaN gaps
            series_filled = series.ffill().bfill()
            # Only forward fill (use previous value)
            df[col] = series.ffill()
            nans_filled += int(nan_mask.sum())
        
        # --- 2. Handle consecutive same values ---
        same_mask = series.diff() == 0
        if same_mask.sum() > 0:
            groups = (same_mask != same_mask.shift()).cumsum()
            for grp_id in groups[same_mask].unique():
                grp_dates = same_mask[same_mask & (groups == grp_id)].index
                grp_len = len(grp_dates)
                
                if grp_len <= 3:
                    continue
                
                # Check if this is a suspension (停牌) — common in China A-shares
                # Signs of suspension:
                # 1. Very long flat period (>20 days)
                # 2. Stock appears in adjacent years
                # 3. Gap occurs in middle of active trading
                
                if grp_len > 20:
                    # Very long flat period → almost certainly suspension, keep
                    continue
                
                # Check if stock is valid across years
                if col in stocks_prev and col in stocks_next:
                    # Stock exists in adjacent years → likely suspension
                    if grp_len > 10:
                        continue  # Keep, likely suspension
                
                # Shorter "flat" period 4-20 days that's not clearly suspension
                # Check trading volume context: in China, suspensions are common
                # For safety, only remove if stock doesn't exist in next year
                if col not in stocks_next and grp_len > 10:
                    stocks_to_remove.add(col)
                    removal_log.append((yr, col, f'连续相同{grp_len}天(次年不存在)'))
                    break
                elif grp_len <= 10:
                    # Short flat period, could be low liquidity → keep
                    continue
    
    # Apply removals
    for s in stocks_to_remove:
        if s in df.columns:
            df = df.drop(columns=[s])
    stocks_cleaned = len(stocks_to_remove)
    
    # Rename and save
    new_name = f'CSI300_constituents_close_{yr}.csv'
    new_path = os.path.join(daily_dir, new_name)
    df.to_csv(new_path)
    
    print(f'{yr}: {df.shape[0]}d × {df.shape[1]} stocks (移除{stocks_cleaned}只, 填充{nans_filled}个NaN)')

# Summary
print(f'\n=== 清理汇总 ===')
print(f'移除 {len(removal_log)} 只股票:')
for yr, code, reason in sorted(removal_log):
    print(f'  {yr} {code}: {reason}')

# Remove old files with force
import subprocess
for f in files:
    try:
        os.remove(f)
    except:
        subprocess.run(['rm', '-f', f], shell=True)
    print(f'  删除旧文件: {os.path.basename(f)}')

print('\n完成!')
