"""
补下载 KOSPI200 2010-2014 年日线数据（yfinance，后复权）
修复版：先取日期交集再判断缺失
"""

import time, sys
from pathlib import Path
import pandas as pd
import yfinance as yf

sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

DATA_DIR = Path(__file__).parent
OUTPUT_DIR = DATA_DIR / "daily_data"
WIDE_CSV = DATA_DIR / "kospi200_constituents_wide.csv"

START_YEAR = 2010
END_YEAR = 2014
MAX_MISSING = 3


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


for year in range(START_YEAR, END_YEAR + 1):
    year_str = str(year)
    output_path = OUTPUT_DIR / f"KOSPI200_constituents_close_{year}.csv"

    # Always redo 2011 since previous run was corrupted
    if year != 2011 and output_path.exists():
        log(f"[SKIP] {year} - 已存在")
        continue

    df_w = pd.read_csv(WIDE_CSV, dtype=str, encoding="utf-8-sig")
    codes = list(dict.fromkeys(str(c).strip() for c in df_w[year_str].dropna() if str(c).strip()))
    log(f"\n{'=' * 50}\n{year}年 — {len(codes)}只成分股 (yfinance)")

    all_data = {}
    ok = fail = 0
    t0 = time.time()
    skipped = []

    for i, code in enumerate(codes):
        try:
            df = yf.Ticker(f"{code}.KS").history(
                start=f"{year}-01-01", end=f"{year}-12-31", auto_adjust=False
            )
            if df is not None and not df.empty:
                close = df["Close"]
                close = close[close > 0]
                if len(close) > 0:
                    close.name = code
                    close.index = pd.to_datetime(close.index.date)
                    all_data[code] = close
                    ok += 1
                else:
                    fail += 1
                    skipped.append(code)
            else:
                fail += 1
                skipped.append(code)
        except:
            fail += 1
            skipped.append(code)

        if (i + 1) % 20 == 0 or i == len(codes) - 1:
            e = time.time() - t0
            r = (i + 1) / e if e > 0 else 0
            eta = (len(codes) - i - 1) / r if r > 0 else 0
            log(f"  [{i + 1}/{len(codes)}] ok={ok} fail={fail} ETA{eta:.0f}s")

    if skipped:
        log(f"  无数据(已退市): {len(skipped)}只")

    if not all_data:
        log(f"  [ERROR] 全部失败!")
        continue

    # Step 1: 合并且只保留所有股票都有数据的日期（交集）
    df_year = pd.DataFrame(all_data)
    df_year.index = pd.to_datetime(df_year.index)
    df_year = df_year.sort_index()

    before_drop = df_year.shape
    df_year = df_year.dropna(how="any")  # 只保留所有列都有值的行
    dropped_rows = before_drop[0] - df_year.shape[0]
    log(f"  日期交集: {before_drop[0]}-{dropped_rows}={df_year.shape[0]}天（删除{dropped_rows}个非共同交易日）")

    if df_year.shape[0] < 200:
        log(f"  [WARN] 共同交易日仅{df_year.shape[0]}天，数据质量差!")

    # Step 2: 删除缺失>3天的股票（在交集日期中仍有NaN的）
    na_counts = df_year.isna().sum()
    if na_counts.sum() > 0:
        bad = na_counts[na_counts > MAX_MISSING]
        if len(bad) > 0:
            log(f"  删除缺失>{MAX_MISSING}天: {len(bad)}只 {list(bad.index)[:5]}...")
            df_year = df_year.drop(columns=bad.index)

    # Step 3: 填充剩余微量缺失
    df_year = df_year.ffill().bfill()

    final_na = df_year.isna().sum().sum()
    df_year.index.name = "Date"
    df_year.to_csv(output_path, encoding="utf-8-sig", float_format="%.0f")
    log(f"  >> {output_path.name} ({df_year.shape[0]}d×{df_year.shape[1]}只, NaN={final_na}, {time.time()-t0:.0f}s)")

log(f"\n完成!")
