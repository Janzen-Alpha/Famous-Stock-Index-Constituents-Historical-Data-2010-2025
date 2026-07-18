"""
CSI 300 历史成分股重建 2010-2025
使用 index-constitution 包 (基于中证指数官网调样公告)
输出按年成分股列表, yfinance兼容格式
"""
import index_constitution as ic
import pandas as pd
import os

print("=== CSI 300 成分股历史重建 ===")

# 1. 获取历史数据
history = ic.history('csi300')
print(f"变动记录: {len(history)} 条")
print(f"唯一股票: {history['symbol'].nunique()} 只")
print(f"时间范围: {history['opt-in'].min().date()} ~ {history['opt-in'].max().date()}")

# 2. 重建每年年末快照
yearly = {}
for year in range(2010, 2026):
    date_str = f'{year}-12-31'
    const = ic.constituents_at('csi300', date_str)
    yearly[year] = sorted(const['symbol'].tolist())
    cnt = len(yearly[year])
    status = '✓' if cnt == 300 else f'({cnt})'
    print(f"{year}: {cnt}只 {status}")

# 3. 转换为 yfinance 格式
def to_yfinance(code):
    if code.startswith('SH'): return code[2:] + '.SS'
    elif code.startswith('SZ'): return code[2:] + '.SZ'
    return code

os.makedirs('data/csi300', exist_ok=True)

# 4. 输出: by_year 格式 (yfinance, 用于下载)
max_len = max(len(yearly[y]) for y in yearly)
output1 = 'data/csi300/CSI300_constituents_by_year.csv'
with open(output1, 'w', encoding='utf-8') as f:
    f.write('year,' + ','.join([f'stock_{i+1}' for i in range(max_len)]) + '\n')
    for y in sorted(yearly):
        codes = [to_yfinance(c) for c in yearly[y]]
        f.write(f'{y},' + ','.join(codes) + '\n')

# 5. 输出: by_year 格式 (原始CSI代码)
output2 = 'data/csi300/CSI300_constituents_by_year_raw.csv'
with open(output2, 'w', encoding='utf-8') as f:
    f.write('year,' + ','.join([f'stock_{i+1}' for i in range(max_len)]) + '\n')
    for y in sorted(yearly):
        f.write(f'{y},' + ','.join(yearly[y]) + '\n')

# 6. 输出: long 格式
output3 = 'data/csi300/CSI300_constituents_long.csv'
rows = []
for y in sorted(yearly):
    for c in yearly[y]:
        rows.append({'year': y, 'code': to_yfinance(c), 'raw_code': c})
pd.DataFrame(rows).to_csv(output3, index=False)

# 7. 输出: matrix 格式
all_codes = sorted(set().union(*yearly.values()))
df = pd.DataFrame([
    {'code': c, **{str(y): (1 if c in yearly[y] else 0) for y in sorted(yearly)}}
    for c in all_codes
]).set_index('code')
df = df[[str(y) for y in sorted(yearly)]]
df.T.to_csv('data/csi300/CSI300_constituents_2010_2025.csv')

print(f"\n输出文件:")
print(f"  {output1}")
print(f"  {output2}")
print(f"  {output3}")
print(f"  data/csi300/CSI300_constituents_2010_2025.csv")

# 8. 验证
print(f"\n=== 验证 ===")
checks = {'SH600519': '贵州茅台', 'SH601318': '中国平安', 'SZ000858': '五粮液'}
for code, name in checks.items():
    yrs_in = [y for y in sorted(yearly) if code in yearly[y]]
    print(f"  {code} ({name}): {yrs_in[0]}-{yrs_in[-1]} ({len(yrs_in)}年)")
print(f"\n总计 unique: {len(all_codes)}只")
