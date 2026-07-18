"""
KOSPI200 历史日线数据下载器
日志输出到 download.log
"""

import time, sys
from pathlib import Path
import pandas as pd
from pykrx import stock

DATA_DIR = Path(__file__).parent
OUTPUT_DIR = DATA_DIR / "daily_data"
WIDE_CSV = DATA_DIR / "kospi200_constituents_wide.csv"
LOG_PATH = DATA_DIR / "download.log"

START_YEAR = 2015
END_YEAR = 2025


def log(msg: str):
    t = time.strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


LOG_PATH.write_text("", encoding="utf-8")

for year in range(START_YEAR, END_YEAR + 1):
    year_str = str(year)
    output_path = OUTPUT_DIR / f"KOSPI200_{year}.csv"
    if output_path.exists():
        log(f"[SKIP] {year}")
        continue

    df_w = pd.read_csv(WIDE_CSV, dtype=str, encoding="utf-8-sig")
    codes = list(dict.fromkeys(str(c).strip() for c in df_w[year_str].dropna() if str(c).strip()))
    log(f"\n{'=' * 50}\n{year}年 — {len(codes)}只")
    all_data, ok, fail = {}, 0, 0
    t0 = time.time()

    for i, code in enumerate(codes):
        try:
            df = stock.get_market_ohlcv(f"{year}0101", f"{year}1231", code)
            if df is not None and not df.empty:
                s = df["종가"]; s.name = code; all_data[code] = s; ok += 1
            else:
                fail += 1
        except:
            fail += 1

        if (i + 1) % 20 == 0 or i == len(codes) - 1:
            e = time.time() - t0
            r = (i + 1) / e if e > 0 else 0
            eta = (len(codes) - i - 1) / r if r > 0 else 0
            log(f"  [{i + 1}/{len(codes)}] ok={ok} fail={fail} ETA{eta:.0f}s")

    if all_data:
        df_out = pd.DataFrame(all_data)
        df_out.index = pd.to_datetime(df_out.index)
        df_out = df_out.sort_index()
        OUTPUT_DIR.mkdir(exist_ok=True)
        df_out.to_csv(output_path, encoding="utf-8-sig", float_format="%.0f")
        log(f"  >> {output_path.name} ({df_out.shape[0]}d×{df_out.shape[1]}只, {time.time()-t0:.0f}s)")

log(f"\n完成! {OUTPUT_DIR}")
