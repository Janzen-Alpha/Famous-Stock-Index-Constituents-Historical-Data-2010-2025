"""
最终清洗 v4: 删除>3 NaN的列，对齐公共日期范围。保守策略。
"""
import pandas as pd, os, glob, re

daily_dir = 'data/csi300/daily'
files = sorted(glob.glob(os.path.join(daily_dir, 'CSI300_*_daily.csv')))
complete_stocks = {}

for f in files:
    yr = int(re.search(r'(\d{4})', f).group(1))
    df = pd.read_csv(f, index_col=0)
    df.index = pd.to_datetime(df.index)
    orig = len(df.columns)
    
    # Step 1: Remove stocks with >3 NaN in their VALID range (exclude start/end gaps)
    bad = []
    for col in list(df.columns):
        s = df[col].dropna()
        if len(s) == 0:
            bad.append(col)
            continue
        # Count NaN ONLY between first and last valid data
        inner = df.loc[s.index[0]:s.index[-1], col]
        nan_inner = inner.isna().sum()
        if nan_inner > 3:
            bad.append(col)
    df = df.drop(columns=bad)
    
    if len(df.columns) == 0:
        print(f'{yr}: ALL removed')
        continue
    
    # Step 2: Remove extreme outliers (stocks with very short valid range)
    while len(df.columns) > 10:
        firsts = [df[c].dropna().index[0] for c in df.columns]
        lasts = [df[c].dropna().index[-1] for c in df.columns]
        spans = [(lasts[i] - firsts[i]).days for i in range(len(firsts))]
        vf, vt = max(firsts), min(lasts)
        common = (vt - vf).days + 1
        median_span = int(pd.Series(spans).median())
        
        if median_span == 0 or common >= median_span * 0.5:
            break
        
        # Find stock with SHORTEST valid range (causes tight common range)
        shortest = min(zip(df.columns, spans), key=lambda x: x[1])
        worst_code, worst_span = shortest
        if worst_span >= median_span * 0.5:  # not really an outlier
            break
        df = df.drop(columns=[worst_code])
        bad.append(worst_code)
    
    # Step 3: Trim to common range, fill
    firsts = [df[c].dropna().index[0] for c in df.columns]
    lasts = [df[c].dropna().index[-1] for c in df.columns]
    vf, vt = max(firsts), min(lasts)
    df = df.loc[vf:vt]
    df = df.ffill().dropna(axis=0)
    
    complete_stocks[yr] = list(df.columns)
    removed = orig - len(df.columns)
    
    print(f'{yr}: {orig}->{len(df.columns)} stocks (删{removed}), {len(df)} days, NaN={df.isna().sum().sum()}')
    
    out = os.path.join(daily_dir, f'CSI300_constituents_close_{yr}.csv')
    df.round(4).to_csv(out)

# Summary
rows = []
for yr in sorted(complete_stocks):
    stocks = complete_stocks[yr]
    r = {'year': yr, 'count': len(stocks)}
    for i, s in enumerate(stocks):
        r[f'stock_{i+1}'] = s
    rows.append(r)
pd.DataFrame(rows).set_index('year').to_csv(os.path.join(daily_dir, 'CSI300_complete_stocks.csv'))

print(f'\n年度: { {yr: len(complete_stocks[yr]) for yr in sorted(complete_stocks)} }')
print('Done!')
