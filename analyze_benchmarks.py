#!/usr/bin/env python3
"""分析五个市场指数benchmark日线数据，计算各年度及全期风险收益指标。"""

import pandas as pd
import numpy as np
import os

BASE_DIR = r".."
BENCH_DIR = os.path.join(BASE_DIR, "指数benchmark数据")
OUTPUT_PATH = os.path.join(BASE_DIR, "README.md")

# 五个市场
MARKETS = {
    "CSI300":   ("沪深300",   os.path.join(BENCH_DIR, "CSI300_daily.csv")),
    "SP500":    ("标普500",   os.path.join(BENCH_DIR, "SP500_daily.csv")),
    "N225":     ("日经225",   os.path.join(BENCH_DIR, "N225_daily.csv")),
    "FTSE100":  ("富时100",   os.path.join(BENCH_DIR, "FTSE100_daily.csv")),
    "KOSPI200": ("韩国KOSPI200", os.path.join(BENCH_DIR, "KOSPI_daily.csv")),
}

RISK_FREE = 0.03  # LPR 3%
TRADING_DAYS = 252

def load_data(path):
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["year"] = df["date"].dt.year
    df["daily_ret"] = df["close"].pct_change()
    return df

def annual_metrics(df, year):
    """计算某一年度的所有指标。"""
    sub = df[df["year"] == year].copy()
    if sub.empty:
        return None
    rets = sub["daily_ret"]
    valid = rets.notna()
    rets_valid = rets[valid]
    if len(rets_valid) < 10:
        return None

    start_close = sub["close"].iloc[0]
    end_close = sub["close"].iloc[-1]
    annual_ret = (end_close / start_close - 1) * 100

    up_days = int((rets_valid > 0).sum())
    down_days = int((rets_valid < 0).sum())
    flat_days = int((rets_valid == 0).sum())

    ann_vol = rets_valid.std() * np.sqrt(TRADING_DAYS) * 100
    excess = rets_valid.mean() * TRADING_DAYS - RISK_FREE
    sharpe = excess / (ann_vol / 100) if ann_vol > 0 else np.nan

    # 最大回撤 (高点和低点日期) — 使用整个 sub 计算，含第一天
    # 构建累计收益：从 sub 第一行开始
    sub2 = sub.copy().reset_index(drop=True)
    cum = (1 + sub2["daily_ret"].fillna(0)).cumprod()
    running_max = cum.cummax()
    drawdown = (cum - running_max) / running_max
    max_dd = drawdown.min() * 100
    dd_end_pos = int(drawdown.idxmin())
    dd_start_pos = int(running_max.iloc[:dd_end_pos + 1].idxmax())
    dd_high_date = sub2["date"].iloc[dd_start_pos]
    dd_low_date = sub2["date"].iloc[dd_end_pos]
    dd_high_val = sub2["close"].iloc[dd_start_pos]
    dd_low_val = sub2["close"].iloc[dd_end_pos]

    return {
        "年": year,
        "收益率(%)": round(annual_ret, 2),
        "上涨天数": up_days,
        "下跌天数": down_days,
        "持平天数": flat_days,
        "夏普率": round(sharpe, 2),
        "波动率(%)": round(ann_vol, 2),
        "最大回撤(%)": round(max_dd, 2),
        "回撤高点日": dd_high_date.strftime("%Y-%m-%d"),
        "回撤低点日": dd_low_date.strftime("%Y-%m-%d"),
        "高点值": round(dd_high_val, 2),
        "低点值": round(dd_low_val, 2),
    }

def full_period_metrics(df):
    """全周期（2010-2025）指标。"""
    rets_valid = df["daily_ret"].dropna()
    if len(rets_valid) < 10:
        return None

    n_years = df["year"].nunique()
    annual_returns = []
    for y in sorted(df["year"].unique()):
        sub = df[df["year"] == y]
        if len(sub) < 10:
            continue
        annual_returns.append(sub["close"].iloc[-1] / sub["close"].iloc[0] - 1)

    avg_annual_ret = np.mean(annual_returns) * 100

    # CAGR
    start_val = df["close"].iloc[0]
    end_val = df["close"].iloc[-1]
    cagr = ((end_val / start_val) ** (1 / n_years) - 1) * 100

    ann_vol = rets_valid.std() * np.sqrt(TRADING_DAYS) * 100
    excess = rets_valid.mean() * TRADING_DAYS - RISK_FREE
    sharpe = excess / (ann_vol / 100) if ann_vol > 0 else np.nan

    # 最大回撤 — 使用整个 df
    df2 = df.copy().reset_index(drop=True)
    cum = (1 + df2["daily_ret"].fillna(0)).cumprod()
    running_max = cum.cummax()
    drawdown = (cum - running_max) / running_max
    max_dd = drawdown.min() * 100
    dd_end_pos = int(drawdown.idxmin())
    dd_start_pos = int(running_max.iloc[:dd_end_pos + 1].idxmax())
    dd_high_date = df2["date"].iloc[dd_start_pos]
    dd_low_date = df2["date"].iloc[dd_end_pos]
    dd_high_val = df2["close"].iloc[dd_start_pos]
    dd_low_val = df2["close"].iloc[dd_end_pos]

    return {
        "年均收益率(%)": round(avg_annual_ret, 2),
        "复合年化CAGR(%)": round(cagr, 2),
        "夏普率(LPR 3%)": round(sharpe, 2),
        "波动率(%)": round(ann_vol, 2),
        "最大回撤(%)": round(max_dd, 2),
        "回撤高点日": dd_high_date.strftime("%Y-%m-%d"),
        "回撤低点日": dd_low_date.strftime("%Y-%m-%d"),
        "高点值": round(dd_high_val, 2),
        "低点值": round(dd_low_val, 2),
    }

# --- 表格格式化函数 ---
def df_to_md(df, col_align=None):
    """将DataFrame转成GitHub风格的Markdown表格。"""
    if col_align is None:
        col_align = {}
    lines = []
    header = "| " + " | ".join(str(c) for c in df.columns) + " |"
    sep = "|"
    for c in df.columns:
        a = col_align.get(c, "---")
        sep += f" {a} |"
    lines.append(header)
    lines.append(sep)
    for _, row in df.iterrows():
        vals = []
        for c in df.columns:
            v = row[c]
            if pd.isna(v):
                vals.append("-")
            elif isinstance(v, float):
                vals.append(f"{v:.2f}")
            else:
                vals.append(str(v))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)

# --- 主流程 ---
all_annual = {}
all_full = {}
market_pairs = []

for code, (name, path) in MARKETS.items():
    df = load_data(path)
    # 年度指标
    records = []
    for y in range(2010, 2026):
        m = annual_metrics(df, y)
        if m:
            records.append(m)
    df_ann = pd.DataFrame(records)
    all_annual[code] = df_ann
    # 全期指标
    fm = full_period_metrics(df)
    all_full[code] = fm
    market_pairs.append((code, name))

# --- 生成 README.md ---
md = []
md.append("# 全球五大市场指数成分股数据集 (2010–2025)")
md.append("")
md.append("## 数据集简介")
md.append("")
md.append("本数据集覆盖**中国（沪深300）、美国（标普500）、日本（日经225）、韩国（KOSPI200）、英国（富时100）**五个主要市场的指数成分股信息，时间跨度为 **2010 年至 2025 年**，共 **16 年**。")
md.append("")
md.append("数据集包含两部分：")
md.append("- **指数 Benchmark 日线行情**（OHLCV），用于计算各市场每年的收益与风险指标。")
md.append("- **各年度成分股完整列表及每日收盘价**，精确到每年有哪些股票在指数中，以及它们该年的逐日收盘价。")
md.append("")
md.append("获取这些每年成分股快照非常不容易——五个市场需要使用不同的数据源和程序，且成分股调整历史信息分散、格式各异，整理与清洗耗费了大量精力。这是一个比较难得的、跨市场可比的长期成分股数据集。")
md.append("")

# ---- 第一部分：各市场年度指标 ----
md.append("---")
md.append("")
md.append("## 一、各指数分年度风险收益指标")
md.append("")
md.append("> 无风险利率统一采用 **3%（LPR）**；波动率为年化波动率（日收益率标准差 × √252）。")
md.append("")

for code, name in market_pairs:
    md.append(f"### {code} — {name}")
    md.append("")
    df_a = all_annual[code]
    # 选需要展示的列
    show_cols = ["年", "收益率(%)", "上涨天数", "下跌天数", "持平天数",
                 "夏普率", "波动率(%)", "最大回撤(%)", "回撤高点日", "回撤低点日"]
    df_show = df_a[show_cols].copy()
    df_show.columns = ["年份", "收益率(%)", "📈 上涨天", "📉 下跌天", "➖ 持平天",
                        "夏普率", "波动率(%)", "最大回撤(%)", "回撤高点", "回撤低点"]
    align = {
        "年份": ":---:", "收益率(%)": "---:", "📈 上涨天": "---:", "📉 下跌天": "---:",
        "➖ 持平天": "---:", "夏普率": "---:", "波动率(%)": "---:",
        "最大回撤(%)": "---:", "回撤高点": ":---:", "回撤低点": ":---:",
    }
    md.append(df_to_md(df_show, align))
    md.append("")

# ---- 第二部分：全期汇总 ----
md.append("---")
md.append("")
md.append("## 二、全周期（2010–2025）汇总指标")
md.append("")

summary_rows = []
for code, name in market_pairs:
    fm = all_full[code]
    summary_rows.append({
        "市场": f"{code} ({name})",
        "年均收益率(%)": fm["年均收益率(%)"],
        "复合年化CAGR(%)": fm["复合年化CAGR(%)"],
        "夏普率(LPR=3%)": fm["夏普率(LPR 3%)"],
        "波动率(%)": fm["波动率(%)"],
        "最大回撤(%)": fm["最大回撤(%)"],
        "回撤区间": f"{fm['回撤高点日']} → {fm['回撤低点日']}",
        "高点值": fm["高点值"],
        "低点值": fm["低点值"],
    })
df_summary = pd.DataFrame(summary_rows)
md.append(df_to_md(df_summary, {
    "市场": ":---", "年均收益率(%)": "---:", "复合年化CAGR(%)": "---:",
    "夏普率(LPR=3%)": "---:", "波动率(%)": "---:", "最大回撤(%)": "---:",
    "回撤区间": ":---:", "高点值": "---:", "低点值": "---:",
}))
md.append("")

# ---- 第三部分：文件结构 ----
md.append("---")
md.append("")
md.append("## 三、文件结构")
md.append("")
md.append("```")
md.append("📁 项目根目录/")
md.append("├── 📁 指数benchmark数据/           # 五市场指数日线行情（OHLCV）")
md.append("│   ├── CSI300_daily.csv           # 沪深300 日线")
md.append("│   ├── SP500_daily.csv            # 标普500 日线")
md.append("│   ├── N225_daily.csv             # 日经225 日线")
md.append("│   ├── FTSE100_daily.csv          # 富时100 日线")
md.append("│   └── KOSPI_daily.csv            # KOSPI200 日线（KOSPI指数）")
md.append("│")
md.append("├── 📁 Yearly_full_constituents_list/  # 每年各市场完整成分股列表")
md.append("│   ├── CSI300_yearly_full_constituents_2010to2025.csv")
md.append("│   ├── SP500_yearly_full_constituents_2010to2025.csv")
md.append("│   ├── N225_yearly_full_constituents_2010to2025.csv")
md.append("│   ├── FTSE100_yearly_full_constituents_2010to2025.csv")
md.append("│   └── KOSPI200_yearly_full_constituents_2010to2025.csv")
md.append("│")
md.append("├── 📁 CSI300_constituents_close_2010to2025/   # 沪深300 各年成分股日收盘价")
md.append("│   ├── CSI300_constituents_close_2010.csv  ...  CSI300_constituents_close_2025.csv")
md.append("│   └── tickers_CSI300_constituents_yearly.csv")
md.append("│")
md.append("├── 📁 SP500_constituents_close_2010to2025/    # 标普500 各年成分股日收盘价")
md.append("│   ├── SP500_constituents_close_2010.csv  ...  SP500_constituents_close_2025.csv")
md.append("│   └── tickers_SP500_constituents_yearly.csv")
md.append("│")
md.append("├── 📁 N225_constituents_close_2010to2025/     # 日经225 各年成分股日收盘价")
md.append("│   ├── N225_constituents_close_2010.csv  ...  N225_constituents_close_2025.csv")
md.append("│   └── tickers_N225_constituents_yearly.csv")
md.append("│")
md.append("├── 📁 FTSE100_constituents_close_2010to2025/  # 富时100 各年成分股日收盘价")
md.append("│   ├── FTSE100_constituents_close_2010.csv  ...  FTSE100_constituents_close_2025.csv")
md.append("│   └── tickers_FTSE100_constituents_yearly.csv")
md.append("│")
md.append("├── 📁 KOSPI200_constituents_close_2010to2025/ # KOSPI200 各年成分股日收盘价")
md.append("│   ├── KOSPI200_constituents_close_2010.csv ... KOSPI200_constituents_close_2025.csv")
md.append("│   └── tickers_KOSPI200_constituents_yearly.csv")
md.append("│")
md.append("└── 📁 codes/                                 # 数据下载与清洗代码")
md.append("    ├── csi300_download_data.py               # 沪深300 成分股获取（东方财富 + akshare）")
md.append("    ├── csi300_clean_data.py / csi300_clean_data2.py  # 沪深300 数据清洗")
md.append("    ├── csi300_reconstract_data.py            # 沪深300 成分股收盘价重建")
md.append("    ├── sp500&ftse100_download_data.py        # 标普500 & 富时100 数据下载（yfinance）")
md.append("    ├── sp500&ftse100_clean_data.py           # 标普500 & 富时100 数据清洗")
md.append("    ├── sp500&ftse100_clean_and_validate.py   # 标普500 & 富时100 校验")
md.append("    ├── n225_download_data.py                 # 日经225 成分股获取（日本交易所 + yfinance）")
md.append("    ├── n225_clean_data.py                    # 日经225 数据清洗")
md.append("    ├── n225_check_and_summary.py             # 日经225 数据校验与汇总")
md.append("    ├── kospi200_download_data_pykrx.py       # KOSPI200 数据下载（pykrx）")
md.append("    ├── kospi200_download_data_yfinance.py    # KOSPI200 数据下载（yfinance备用）")
md.append("    ├── kospi200_aggregate.py                 # KOSPI200 成分股聚合")
md.append("    └── kospi200_clean_data.py                # KOSPI200 数据清洗")
md.append("```")
md.append("")

# ---- 第四部分：数据获取说明 ----
md.append("---")
md.append("")
md.append("## 四、数据获取说明")
md.append("")
md.append("五个市场使用了**完全不同的数据源和工具链**：")
md.append("")
md.append("| 市场 | 指数 | 数据源 | 主要工具 |")
md.append("|:---|:---|:---|:---|")
md.append("| 中国 | 沪深300 (CSI300) | 东方财富、AKShare | `akshare` |")
md.append("| 美国 | 标普500 (S&P500) | Yahoo Finance | `yfinance` |")
md.append("| 日本 | 日经225 (Nikkei 225) | 日本交易所集团、Yahoo Finance | `jpxtray`, `yfinance` |")
md.append("| 韩国 | KOSPI200 | KRX（韩国交易所）、Yahoo Finance | `pykrx`, `yfinance` |")
md.append("| 英国 | 富时100 (FTSE100) | Yahoo Finance | `yfinance` |")
md.append("")
md.append("各市场的成分股调整规则和历史数据格式差异巨大：")
md.append("- **沪深300** 每半年调整一次，历史成分股数据需从东方财富逐步获取并重建。")
md.append("- **标普500** 采用季度调整，成分股变动频繁，需要通过维基百科历史快照交叉验证。")
md.append("- **日经225** 成分股调整不规则，部分年份有大幅替换，且日股代码体系（4位数字）与 ticker 映射需要特殊处理。")
md.append("- **KOSPI200** 每年6月和12月调整，韩股代码需要从 KRX 信息数据系统获取，且 pykrx 对环境依赖较强。")
md.append("- **富时100** 每季度调整，通过 yfinance 获取历史成分股时需注意退市和代码变更问题。")
md.append("")

# ---- 第五部分：数据格式说明 ----
md.append("---")
md.append("")
md.append("## 五、数据格式说明")
md.append("")
md.append("### 指数 Benchmark 日线 (`指数benchmark数据/`)")
md.append("")
md.append("每个 CSV 包含以下列：`date, open, high, low, close, volume`（FTSE100 不含 volume）。")
md.append("日期格式：`YYYY/M/D`。")
md.append("")
md.append("### 年度成分股列表 (`Yearly_full_constituents_list/`)")
md.append("")
md.append("每个 CSV 第一行为年份行（2010, 2011, ..., 2025），下方每行对应一只股票在各年的代码。")
md.append("若某年该股票不在指数中，对应格为空。")
md.append("")
md.append("### 成分股收盘价 (`*_constituents_close_2010to2025/`)")
md.append("")
md.append("每年一个 CSV，列为 `Date, Ticker1, Ticker2, ...`，行为该年的每个交易日，内容为当日收盘价。")
md.append("")

# ---- 第六部分：使用建议 ----
md.append("---")
md.append("")
md.append("## 六、使用建议与引用")
md.append("")
md.append("- 该数据集可用于跨市场因子研究、指数构建回测、成分股变动事件研究等。")
md.append("- 请留意各市场交易日期不完全重叠（节假日不同），在进行跨市场比较时需对齐日期。")
md.append("- 若在研究中使用了本数据集，欢迎引用本仓库。")
md.append("")
md.append("---")
md.append("")
md.append(f"*最后更新: 2025-07-18*")
md.append("")

final_md = "\n".join(md)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(final_md)

print(f"✅ README.md 已生成: {OUTPUT_PATH}")
print(f"   包含五个市场 {len(all_annual)} 组年度指标 + 全周期汇总表")
