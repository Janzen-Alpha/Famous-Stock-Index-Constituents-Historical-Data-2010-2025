"""
KOSPI200 数据清洗 + 成分股清单生成
1. 检查每年每只股票的缺失值（同一年的股票行数必须一致）
2. 缺失超过3天的股票删除整列
3. 重命名为 KOSPI200_constituents_close_YYYY.csv
4. 生成成分股汇总CSV（格式参考 tickers_CSI300_constituents_yearly.csv）
"""

import pandas as pd
from pathlib import Path
import sys

sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

DATA_DIR = Path(__file__).parent / "daily_data"
OUTPUT_DIR = Path(__file__).parent / "daily_data"
MAX_MISSING = 3  # 允许的最大缺失天数


def log(msg: str):
    print(msg, flush=True)


# ============================================================
# Step 1: 清洗每年数据
# ============================================================
log("=" * 60)
log("Step 1: 数据清洗（删除缺失>3天的股票）")
log("=" * 60)

all_years = []
all_clean_codes = {}  # year -> list of codes

for f in sorted(DATA_DIR.glob("KOSPI200_????.csv")):
    year = f.stem.split("_")[1]
    df = pd.read_csv(f, index_col=0, encoding="utf-8-sig")
    
    original_cols = len(df.columns)
    
    # 统计每只股票的非NaN行数
    counts = df.notna().sum()
    max_count = counts.max()
    
    # 找出缺失超过3天的股票
    bad_codes = counts[counts < max_count - MAX_MISSING].index.tolist()
    
    if bad_codes:
        log(f"\n{year}年: 原始{original_cols}只, 删除{len(bad_codes)}只 (缺失>{MAX_MISSING}天):")
        for code in bad_codes:
            na_count = max_count - counts[code]
            log(f"  - {code}: 缺失{na_count}天")
        df = df.drop(columns=bad_codes)
    else:
        log(f"\n{year}年: 原始{original_cols}只, 全部通过 (0只删除)")
    
    # 确保所有保留的股票行数一致（用 forward fill 补少量缺失）
    # 先取所有股票都有值的日期（交集），保证完全一致
    # 但更实用的做法：保留 max_count 的日期，少数缺失用 ffill
    # 这里用日期索引的交集方式：
    valid_mask = df.notna().all(axis=1)
    n_all_valid = valid_mask.sum()
    n_total = len(df)
    
    if n_all_valid < n_total:
        # 有少数日期部分股票缺失，用前向填充补
        log(f"  微量缺失处理: {n_total - n_all_valid}行有NaN → ffill填充")
        df = df.ffill().bfill()  # 前向+后向填充
    else:
        log(f"  数据完整: {n_all_valid}/{n_total}行全部有值")
    
    # 验证：所有列NaN数应为0
    remaining_na = df.isna().sum().sum()
    if remaining_na > 0:
        log(f"  [WARN] 仍有{remaining_na}个NaN!")
    
    clean_codes = sorted(df.columns.tolist())
    all_clean_codes[year] = clean_codes
    all_years.append((year, df))
    
    # 保存清洗后的文件
    out_path = OUTPUT_DIR / f"KOSPI200_constituents_close_{year}.csv"
    df.to_csv(out_path, encoding="utf-8-sig", float_format="%.0f")
    log(f"  → {out_path.name} ({df.shape[0]}天 × {df.shape[1]}只)")


# ============================================================
# Step 2: 生成成分股汇总CSV（参考 CSI300 格式）
# ============================================================
log(f"\n{'=' * 60}")
log("Step 2: 生成成分股汇总表")
log("=" * 60)

years_sorted = sorted(all_clean_codes.keys())
max_len = max(len(codes) for codes in all_clean_codes.values())

ticker_csv = OUTPUT_DIR / "tickers_KOSPI200_constituents_yearly.csv"

with open(ticker_csv, "w", encoding="utf-8-sig", newline="") as f_out:
    import csv
    writer = csv.writer(f_out)
    
    # 第一行：年份
    writer.writerow(years_sorted)
    
    # 后续行：每行对应一个位置，各年的代码对齐
    for i in range(max_len):
        row = []
        for year in years_sorted:
            codes = all_clean_codes[year]
            row.append(codes[i] if i < len(codes) else "")
        writer.writerow(row)

log(f"  → {ticker_csv.name} ({max_len}行 × {len(years_sorted)}列)")

# ============================================================
# Step 3: 汇总统计
# ============================================================
log(f"\n{'=' * 60}")
log("最终汇总")
log("=" * 60)
log(f"{'年份':<8} {'股票数':<8} {'交易日':<8}")
log("-" * 30)
for year, df in all_years:
    log(f"{year:<8} {df.shape[1]:<8} {df.shape[0]:<8}")

# 年份间的成分股连续性（有多少只在相邻年份都出现）
log(f"\n年份连续性:")
for i in range(1, len(years_sorted)):
    prev = set(all_clean_codes[years_sorted[i-1]])
    curr = set(all_clean_codes[years_sorted[i]])
    overlap = prev & curr
    log(f"  {years_sorted[i-1]}→{years_sorted[i]}: {len(overlap)}只连续")

# 统计符号总数
all_unique = set()
for codes in all_clean_codes.values():
    all_unique.update(codes)
log(f"\n全部去重代码: {len(all_unique)}只")
log(f"出现在所有年份: {len(set.intersection(*[set(c) for c in all_clean_codes.values()]))}只")

log(f"\n完成!")
