**English** | [中文](README_CN.md)

# Global Five-Market Index Constituent Dataset (2010–2025)

## Overview

This dataset covers index constituent data for **five major markets — China (CSI 300), United States (S&P 500), Japan (Nikkei 225), South Korea (KOSPI 200), and United Kingdom (FTSE 100)** — spanning **16 years from 2010 to 2025**.

The dataset consists of two parts:
- **Index Benchmark Daily OHLCV Data**, used to compute annual return and risk metrics for each market.
- **Full Yearly Constituent Lists & Daily Close Prices**, detailing exactly which stocks were in each index each year, along with their daily closing prices.

Compiling these annual constituent snapshots was no small effort — the five markets required entirely different data sources and tools, with constituent adjustment histories scattered across disparate formats. Cleaning and reconciling this data took considerable work. This is a hard-won, cross-market comparable, long-horizon constituent dataset.

---

## 1. Annual Risk & Return Metrics by Index

> Risk-free rate uniformly set at **3% (LPR)**; volatility is annualized (daily return std dev × √252).

### CSI 300

| Year | Return(%) | 📈 Up Days | 📉 Down Days | ➖ Flat | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | -11.51 | 122 | 119 | 0 | -0.50 | 25.16 | -29.50 | 2010-01-05 | 2010-07-05 |
| 2011 | -26.46 | 115 | 129 | 0 | -1.48 | 20.66 | -31.64 | 2011-04-13 | 2011-12-27 |
| 2012 | 9.75 | 119 | 124 | 0 | 0.32 | 20.44 | -22.41 | 2012-05-07 | 2012-12-03 |
| 2013 | -7.70 | 114 | 124 | 0 | -0.40 | 22.22 | -22.16 | 2013-02-06 | 2013-06-27 |
| 2014 | 52.19 | 130 | 115 | 0 | 2.17 | 19.25 | -10.12 | 2014-01-02 | 2014-03-20 |
| 2015 | 2.46 | 138 | 106 | 0 | 0.27 | 39.43 | -43.48 | 2015-06-08 | 2015-08-26 |
| 2016 | -4.58 | 127 | 117 | 0 | -0.58 | 22.22 | -19.38 | 2016-01-06 | 2016-01-28 |
| 2017 | 20.60 | 137 | 107 | 0 | 1.76 | 10.15 | -6.07 | 2017-11-22 | 2017-12-07 |
| 2018 | -26.34 | 114 | 129 | 0 | -1.44 | 21.42 | -31.88 | 2018-01-24 | 2018-12-27 |
| 2019 | 37.95 | 127 | 117 | 0 | 1.55 | 19.85 | -13.49 | 2019-04-19 | 2019-06-06 |
| 2020 | 25.51 | 137 | 106 | 0 | 1.08 | 22.77 | -16.08 | 2020-03-05 | 2020-03-23 |
| 2021 | -6.21 | 127 | 116 | 0 | -0.37 | 18.59 | -18.19 | 2021-02-10 | 2021-07-27 |
| 2022 | -21.27 | 111 | 131 | 0 | -1.29 | 20.41 | -28.65 | 2022-01-04 | 2022-10-31 |
| 2023 | -11.75 | 107 | 135 | 0 | -1.09 | 13.50 | -21.51 | 2023-01-30 | 2023-12-20 |
| 2024 | 16.20 | 119 | 123 | 0 | 0.63 | 21.39 | -14.41 | 2024-05-20 | 2024-09-13 |
| 2025 | 21.19 | 135 | 108 | 0 | 0.99 | 15.26 | -10.49 | 2025-03-19 | 2025-04-07 |

### S&P 500

| Year | Return(%) | 📈 Up Days | 📉 Down Days | ➖ Flat | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | 11.00 | 143 | 108 | 0 | 0.50 | 18.02 | -15.99 | 2010-04-23 | 2010-07-02 |
| 2011 | -1.12 | 138 | 114 | 0 | -0.01 | 23.27 | -19.39 | 2011-04-29 | 2011-10-03 |
| 2012 | 11.68 | 132 | 118 | 2 | 0.82 | 12.72 | -9.94 | 2012-04-02 | 2012-06-01 |
| 2013 | 26.39 | 147 | 105 | 0 | 2.13 | 11.07 | -5.76 | 2013-05-21 | 2013-06-24 |
| 2014 | 12.39 | 144 | 108 | 0 | 0.74 | 11.37 | -7.40 | 2014-09-18 | 2014-10-15 |
| 2015 | -0.69 | 119 | 133 | 0 | -0.16 | 15.49 | -12.35 | 2015-05-21 | 2015-08-25 |
| 2016 | 11.24 | 131 | 121 | 1 | 0.53 | 13.07 | -9.30 | 2016-01-05 | 2016-02-11 |
| 2017 | 18.42 | 143 | 107 | 1 | 2.25 | 6.68 | -2.80 | 2017-03-01 | 2017-04-13 |
| 2018 | -7.01 | 133 | 118 | 0 | -0.47 | 17.08 | -19.78 | 2018-09-20 | 2018-12-24 |
| 2019 | 28.71 | 150 | 102 | 0 | 1.86 | 12.47 | -6.84 | 2019-04-30 | 2019-06-03 |
| 2020 | 15.29 | 145 | 108 | 0 | 0.52 | 34.43 | -33.92 | 2020-02-19 | 2020-03-23 |
| 2021 | 28.79 | 143 | 109 | 0 | 1.66 | 13.10 | -5.21 | 2021-09-02 | 2021-10-04 |
| 2022 | -19.95 | 108 | 143 | 0 | -0.90 | 24.17 | -25.43 | 2022-01-03 | 2022-10-12 |
| 2023 | 24.73 | 137 | 113 | 0 | 1.51 | 13.09 | -10.28 | 2023-07-31 | 2023-10-27 |
| 2024 | 24.01 | 143 | 109 | 0 | 1.48 | 12.65 | -8.49 | 2024-07-16 | 2024-08-05 |
| 2025 | 16.65 | 144 | 106 | 0 | 0.75 | 18.75 | -18.90 | 2025-02-19 | 2025-04-08 |

### Nikkei 225

| Year | Return(%) | 📈 Up Days | 📉 Down Days | ➖ Flat | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | -4.00 | 121 | 121 | 0 | -0.24 | 21.03 | -22.18 | 2010-04-05 | 2010-08-31 |
| 2011 | -18.68 | 124 | 121 | 0 | -0.84 | 23.50 | -24.84 | 2011-02-21 | 2011-11-25 |
| 2012 | 21.44 | 130 | 118 | 0 | 1.19 | 16.26 | -19.11 | 2012-03-27 | 2012-06-04 |
| 2013 | 52.42 | 137 | 108 | 0 | 1.74 | 26.94 | -20.36 | 2013-05-22 | 2013-06-13 |
| 2014 | 9.69 | 129 | 115 | 0 | 0.30 | 20.38 | -13.72 | 2014-01-08 | 2014-04-14 |
| 2015 | 9.33 | 139 | 105 | 0 | 0.39 | 21.16 | -18.87 | 2015-06-24 | 2015-09-29 |
| 2016 | 3.60 | 128 | 117 | 0 | 0.04 | 27.15 | -18.96 | 2016-01-04 | 2016-06-24 |
| 2017 | 16.18 | 129 | 118 | 0 | 1.31 | 11.90 | -6.61 | 2017-03-13 | 2017-04-14 |
| 2018 | -14.85 | 128 | 117 | 1 | -0.74 | 19.26 | -21.07 | 2018-10-02 | 2018-12-25 |
| 2019 | 20.93 | 135 | 106 | 0 | 1.12 | 13.84 | -9.17 | 2019-04-25 | 2019-08-26 |
| 2020 | 18.27 | 122 | 120 | 0 | 0.61 | 25.99 | -31.27 | 2020-01-20 | 2020-03-19 |
| 2021 | 5.63 | 125 | 120 | 0 | 0.20 | 18.61 | -11.34 | 2021-02-16 | 2021-08-20 |
| 2022 | -10.95 | 126 | 118 | 0 | -0.54 | 20.43 | -15.73 | 2022-01-05 | 2022-03-09 |
| 2023 | 30.13 | 142 | 104 | 0 | 1.48 | 16.06 | -9.56 | 2023-07-03 | 2023-10-04 |
| 2024 | 19.85 | 130 | 115 | 0 | 0.71 | 26.07 | -25.50 | 2024-07-11 | 2024-08-05 |
| 2025 | 28.07 | 134 | 109 | 0 | 1.00 | 23.92 | -22.32 | 2025-01-07 | 2025-04-07 |

### FTSE 100

| Year | Return(%) | 📈 Up Days | 📉 Down Days | ➖ Flat | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | 7.27 | 131 | 121 | 0 | 0.32 | 17.40 | -17.50 | 2010-04-15 | 2010-07-01 |
| 2011 | -7.34 | 124 | 127 | 0 | -0.30 | 21.30 | -18.83 | 2011-02-08 | 2011-10-04 |
| 2012 | 3.47 | 127 | 123 | 1 | 0.26 | 14.01 | -11.82 | 2012-03-16 | 2012-06-01 |
| 2013 | 11.97 | 143 | 110 | 0 | 0.92 | 12.17 | -11.86 | 2013-05-22 | 2013-06-24 |
| 2014 | -2.26 | 132 | 120 | 1 | -0.45 | 11.36 | -10.12 | 2014-05-14 | 2014-12-15 |
| 2015 | -4.67 | 128 | 123 | 2 | -0.38 | 17.27 | -17.31 | 2015-04-27 | 2015-12-14 |
| 2016 | 17.22 | 138 | 115 | 0 | 0.70 | 16.83 | -9.78 | 2016-01-05 | 2016-02-11 |
| 2017 | 7.10 | 131 | 121 | 0 | 0.55 | 8.56 | -4.40 | 2017-06-02 | 2017-09-15 |
| 2018 | -12.03 | 126 | 127 | 0 | -1.22 | 12.70 | -16.41 | 2018-05-22 | 2018-12-27 |
| 2019 | 12.00 | 137 | 116 | 0 | 0.77 | 11.73 | -8.06 | 2019-07-29 | 2019-08-15 |
| 2020 | -15.04 | 133 | 120 | 0 | -0.48 | 29.31 | -34.93 | 2020-01-17 | 2020-03-23 |
| 2021 | 12.36 | 135 | 118 | 0 | 0.87 | 12.75 | -6.78 | 2021-01-08 | 2021-01-29 |
| 2022 | -0.71 | 136 | 113 | 1 | -0.04 | 16.45 | -11.03 | 2022-02-10 | 2022-10-12 |
| 2023 | 2.37 | 136 | 115 | 0 | 0.12 | 11.56 | -9.45 | 2023-02-20 | 2023-07-07 |
| 2024 | 5.85 | 132 | 122 | 0 | 0.31 | 9.40 | -5.18 | 2024-05-15 | 2024-08-05 |
| 2025 | 20.35 | 149 | 103 | 0 | 1.44 | 12.03 | -13.43 | 2025-03-03 | 2025-04-09 |

### KOSPI 200

| Year | Return(%) | 📈 Up Days | 📉 Down Days | ➖ Flat | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | 21.34 | 137 | 105 | 2 | 1.14 | 16.09 | -10.80 | 2010-04-26 | 2010-05-25 |
| 2011 | -13.05 | 117 | 121 | 0 | -0.46 | 28.05 | -27.48 | 2011-05-02 | 2011-09-26 |
| 2012 | 7.36 | 119 | 118 | 1 | 0.54 | 17.27 | -14.30 | 2012-04-03 | 2012-07-25 |
| 2013 | -1.83 | 113 | 123 | 2 | -0.13 | 14.05 | -13.98 | 2013-01-02 | 2013-06-26 |
| 2014 | -5.27 | 120 | 124 | 0 | -0.93 | 11.37 | -11.55 | 2014-07-30 | 2014-10-17 |
| 2015 | -1.80 | 127 | 119 | 2 | -0.29 | 12.95 | -18.73 | 2015-04-23 | 2015-08-24 |
| 2016 | 10.82 | 129 | 115 | 0 | 0.46 | 12.98 | -5.22 | 2016-01-05 | 2016-01-21 |
| 2017 | 23.49 | 137 | 100 | 1 | 2.01 | 10.50 | -5.99 | 2017-07-24 | 2017-08-11 |
| 2018 | -19.64 | 122 | 120 | 2 | -1.62 | 14.88 | -23.03 | 2018-01-29 | 2018-10-29 |
| 2019 | 13.76 | 134 | 111 | 1 | 0.71 | 13.55 | -13.29 | 2019-04-16 | 2019-08-07 |
| 2020 | 34.08 | 153 | 95 | 0 | 1.03 | 28.87 | -34.89 | 2020-01-22 | 2020-03-19 |
| 2021 | -1.42 | 125 | 123 | 0 | -0.01 | 17.50 | -15.25 | 2021-06-25 | 2021-11-30 |
| 2022 | -26.38 | 113 | 130 | 1 | -1.68 | 19.31 | -28.84 | 2022-01-04 | 2022-09-30 |
| 2023 | 23.53 | 127 | 118 | 0 | 1.24 | 15.70 | -12.95 | 2023-08-01 | 2023-10-31 |
| 2024 | -11.85 | 119 | 125 | 0 | -0.62 | 21.16 | -21.27 | 2024-07-11 | 2024-12-09 |
| 2025 | 90.70 | 150 | 91 | 1 | 2.87 | 23.37 | -14.26 | 2025-03-21 | 2025-04-09 |

---

## 2. Full-Period Summary (2010–2025)

| Market | Avg Annual Return(%) | CAGR(%) | Sharpe (LPR=3%) | Volatility(%) | Max DD(%) | DD Interval | Peak Value | Trough Value |
| :--- | ---: | ---: | ---: | ---: | ---: | :---: | ---: | ---: |
| CSI 300 | 4.38 | 1.70 | 0.05 | 21.65 | -46.70 | 2015-06-08 → 2016-01-28 | 5353.75 | 2853.76 |
| S&P 500 | 12.53 | 11.90 | 0.56 | 17.32 | -33.92 | 2020-02-19 → 2020-03-23 | 3386.15 | 2237.40 |
| Nikkei 225 | 11.69 | 10.19 | 0.44 | 21.25 | -31.80 | 2018-10-02 → 2020-03-19 | 24270.62 | 16552.83 |
| FTSE 100 | 3.62 | 3.77 | 0.12 | 15.48 | -36.61 | 2018-05-22 → 2020-03-23 | 7877.50 | 4993.90 |
| KOSPI 200 | 8.99 | 6.43 | 0.28 | 18.18 | -41.19 | 2017-11-03 → 2020-03-19 | 338.83 | 199.28 |

---

## 3. File Structure

```
📁 Project Root/
├── 📁 Index benchmark data/              # Index benchmark daily OHLCV data
│   ├── CSI300_daily.csv              # CSI 300 daily
│   ├── SP500_daily.csv               # S&P 500 daily
│   ├── N225_daily.csv                # Nikkei 225 daily
│   ├── FTSE100_daily.csv             # FTSE 100 daily
│   └── KOSPI_daily.csv               # KOSPI 200 daily
│
├── 📁 Yearly_full_constituents_list/  # Full yearly constituent lists
│   ├── CSI300_yearly_full_constituents_2010to2025.csv
│   ├── SP500_yearly_full_constituents_2010to2025.csv
│   ├── N225_yearly_full_constituents_2010to2025.csv
│   ├── FTSE100_yearly_full_constituents_2010to2025.csv
│   └── KOSPI200_yearly_full_constituents_2010to2025.csv
│
├── 📁 CSI300_constituents_close_2010to2025/   # CSI 300 daily close prices
│   ├── CSI300_constituents_close_2010.csv ... CSI300_constituents_close_2025.csv
│   └── tickers_CSI300_constituents_yearly.csv
│
├── 📁 SP500_constituents_close_2010to2025/    # S&P 500 daily close prices
│   ├── SP500_constituents_close_2010.csv ... SP500_constituents_close_2025.csv
│   └── tickers_SP500_constituents_yearly.csv
│
├── 📁 N225_constituents_close_2010to2025/     # Nikkei 225 daily close prices
│   ├── N225_constituents_close_2010.csv ... N225_constituents_close_2025.csv
│   └── tickers_N225_constituents_yearly.csv
│
├── 📁 FTSE100_constituents_close_2010to2025/  # FTSE 100 daily close prices
│   ├── FTSE100_constituents_close_2010.csv ... FTSE100_constituents_close_2025.csv
│   └── tickers_FTSE100_constituents_yearly.csv
│
├── 📁 KOSPI200_constituents_close_2010to2025/ # KOSPI 200 daily close prices
│   ├── KOSPI200_constituents_close_2010.csv ... KOSPI200_constituents_close_2025.csv
│   └── tickers_KOSPI200_constituents_yearly.csv
│
└── 📁 codes/                                  # Data download & cleaning scripts
    ├── csi300_download_data.py                # CSI 300 constituent download (Eastmoney + akshare)
    ├── csi300_clean_data.py / csi300_clean_data2.py  # CSI 300 data cleaning
    ├── csi300_reconstract_data.py             # CSI 300 close price reconstruction
    ├── sp500&ftse100_download_data.py         # S&P 500 & FTSE 100 download (yfinance)
    ├── sp500&ftse100_clean_data.py            # S&P 500 & FTSE 100 data cleaning
    ├── sp500&ftse100_clean_and_validate.py    # S&P 500 & FTSE 100 validation
    ├── n225_download_data.py                  # Nikkei 225 download (JPX + yfinance)
    ├── n225_clean_data.py                     # Nikkei 225 data cleaning
    ├── n225_check_and_summary.py              # Nikkei 225 validation & summary
    ├── kospi200_download_data_pykrx.py        # KOSPI 200 download (pykrx)
    ├── kospi200_download_data_yfinance.py     # KOSPI 200 download (yfinance fallback)
    ├── kospi200_aggregate.py                  # KOSPI 200 constituent aggregation
    └── kospi200_clean_data.py                 # KOSPI 200 data cleaning
```

---

## 4. Data Sources & Methodology

The five markets required **entirely different data sources and toolchains**:

| Market | Index | Data Source | Primary Tool |
|:---|:---|:---|:---|
| China | CSI 300 | Eastmoney, AKShare | `akshare` |
| United States | S&P 500 | Yahoo Finance | `yfinance` |
| Japan | Nikkei 225 | Japan Exchange Group, Yahoo Finance | `jpxtray`, `yfinance` |
| South Korea | KOSPI 200 | KRX (Korea Exchange), Yahoo Finance | `pykrx`, `yfinance` |
| United Kingdom | FTSE 100 | Yahoo Finance | `yfinance` |

Constituent adjustment rules and historical data formats vary dramatically across markets:
- **CSI 300** adjusts semi-annually; historical constituent data had to be incrementally fetched and reconstructed from Eastmoney.
- **S&P 500** adjusts quarterly with frequent constituent changes, requiring cross-validation against Wikipedia historical snapshots.
- **Nikkei 225** has irregular adjustment schedules with major replacements in certain years; Japanese 4-digit ticker codes required special mapping.
- **KOSPI 200** adjusts each June and December; Korean stock codes required retrieval from the KRX information system, and `pykrx` has strong environment dependencies.
- **FTSE 100** adjusts quarterly; delisted stocks and ticker changes require careful handling when fetching via `yfinance`.

---

## 5. Data Format

### Index Benchmark Daily Data (`指数benchmark数据/`)

Each CSV contains columns: `date, open, high, low, close, volume` (FTSE 100 excludes volume).
Date format: `YYYY/M/D`.

### Yearly Constituent Lists (`Yearly_full_constituents_list/`)

Each CSV has a header row of years (2010, 2011, ..., 2025), with each subsequent row representing one stock's ticker code per year. If a stock was not in the index in a given year, the corresponding cell is empty.

### Constituent Close Prices (`*_constituents_close_2010to2025/`)

One CSV per year, with columns `Date, Ticker1, Ticker2, ...` and rows representing each trading day. Cell values are daily closing prices.

---

## 6. Usage & Citation

- This dataset is suitable for cross-market factor research, index construction backtesting, and constituent-change event studies.
- Note that trading calendars are not fully aligned across markets (different holidays); align dates when performing cross-market comparisons.
- If you use this dataset in your research, we'd appreciate a citation to this repository.

---

*Last updated: 2026-07-18*
