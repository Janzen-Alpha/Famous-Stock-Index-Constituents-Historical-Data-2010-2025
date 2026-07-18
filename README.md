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

| Year | Start | End | Return(%) | 📈 Up Days | 📉 Down Days | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | 3535.23 | 3128.26 | -11.51 | 122 | 119 | -0.50 | 25.16 | -29.50 | 2010-01-05 | 2010-07-05 |
| 2011 | 3189.68 | 2345.74 | -26.46 | 114 | 129 | -1.59 | 20.60 | -31.64 | 2011-04-13 | 2011-12-27 |
| 2012 | 2298.75 | 2522.95 | 9.75 | 119 | 123 | 0.43 | 20.37 | -22.41 | 2012-05-07 | 2012-12-03 |
| 2013 | 2524.41 | 2330.03 | -7.70 | 113 | 124 | -0.41 | 22.27 | -22.16 | 2013-02-06 | 2013-06-27 |
| 2014 | 2321.98 | 3533.70 | 52.19 | 130 | 114 | 2.19 | 19.29 | -10.12 | 2014-01-02 | 2014-03-20 |
| 2015 | 3641.54 | 3731.00 | 2.46 | 137 | 106 | 0.19 | 39.39 | -43.48 | 2015-06-08 | 2015-08-26 |
| 2016 | 3469.07 | 3310.08 | -4.58 | 127 | 116 | -0.27 | 21.09 | -19.38 | 2016-01-06 | 2016-01-28 |
| 2017 | 3342.23 | 4030.85 | 20.60 | 136 | 107 | 1.67 | 10.13 | -6.07 | 2017-11-22 | 2017-12-07 |
| 2018 | 4087.40 | 3010.65 | -26.34 | 113 | 129 | -1.52 | 21.41 | -31.88 | 2018-01-24 | 2018-12-27 |
| 2019 | 2969.54 | 4096.58 | 37.95 | 127 | 116 | 1.63 | 19.84 | -13.49 | 2019-04-19 | 2019-06-06 |
| 2020 | 4152.24 | 5211.29 | 25.51 | 136 | 106 | 1.02 | 22.78 | -16.08 | 2020-03-05 | 2020-03-23 |
| 2021 | 5267.72 | 4940.37 | -6.21 | 126 | 116 | -0.43 | 18.59 | -18.19 | 2021-02-10 | 2021-07-27 |
| 2022 | 4917.77 | 3871.63 | -21.27 | 111 | 130 | -1.27 | 20.44 | -28.65 | 2022-01-04 | 2022-10-31 |
| 2023 | 3887.90 | 3431.11 | -11.75 | 106 | 135 | -1.12 | 13.52 | -21.51 | 2023-01-30 | 2023-12-20 |
| 2024 | 3386.35 | 3934.91 | 16.20 | 119 | 122 | 0.70 | 21.38 | -14.41 | 2024-05-20 | 2024-09-13 |
| 2025 | 3820.40 | 4629.94 | 21.19 | 135 | 107 | 1.21 | 14.99 | -10.49 | 2025-03-19 | 2025-04-07 |

### S&P 500

| Year | Start | End | Return(%) | 📈 Up Days | 📉 Down Days | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | 1132.99 | 1257.64 | 11.00 | 143 | 108 | 0.50 | 18.02 | -15.99 | 2010-04-23 | 2010-07-02 |
| 2011 | 1271.87 | 1257.60 | -1.12 | 137 | 114 | -0.06 | 23.29 | -19.39 | 2011-04-29 | 2011-10-03 |
| 2012 | 1277.06 | 1426.19 | 11.68 | 131 | 118 | 0.70 | 12.65 | -9.94 | 2012-04-02 | 2012-06-01 |
| 2013 | 1462.42 | 1848.36 | 26.39 | 146 | 105 | 1.95 | 10.82 | -5.76 | 2013-05-21 | 2013-06-24 |
| 2014 | 1831.98 | 2058.90 | 12.39 | 144 | 107 | 0.83 | 11.35 | -7.40 | 2014-09-18 | 2014-10-15 |
| 2015 | 2058.20 | 2043.94 | -0.69 | 119 | 132 | -0.16 | 15.52 | -12.35 | 2015-05-21 | 2015-08-25 |
| 2016 | 2012.66 | 2238.83 | 11.24 | 131 | 120 | 0.65 | 13.00 | -9.30 | 2016-01-05 | 2016-02-11 |
| 2017 | 2257.83 | 2673.61 | 18.42 | 142 | 107 | 2.14 | 6.65 | -2.80 | 2017-03-01 | 2017-04-13 |
| 2018 | 2695.81 | 2506.85 | -7.01 | 132 | 118 | -0.52 | 17.10 | -19.78 | 2018-09-20 | 2018-12-24 |
| 2019 | 2510.03 | 3230.78 | 28.71 | 149 | 102 | 1.85 | 12.49 | -6.84 | 2019-04-30 | 2019-06-03 |
| 2020 | 3257.85 | 3756.07 | 15.29 | 144 | 108 | 0.50 | 34.49 | -33.92 | 2020-02-19 | 2020-03-23 |
| 2021 | 3700.65 | 4766.18 | 28.79 | 143 | 108 | 1.79 | 13.03 | -5.21 | 2021-09-02 | 2021-10-04 |
| 2022 | 4796.56 | 3839.50 | -19.95 | 107 | 143 | -0.93 | 24.21 | -25.43 | 2022-01-03 | 2022-10-12 |
| 2023 | 3824.14 | 4769.83 | 24.73 | 137 | 112 | 1.54 | 13.11 | -10.28 | 2023-07-31 | 2023-10-27 |
| 2024 | 4742.83 | 5881.63 | 24.01 | 143 | 108 | 1.53 | 12.66 | -8.49 | 2024-07-16 | 2024-08-05 |
| 2025 | 5868.55 | 6845.50 | 16.65 | 144 | 105 | 0.76 | 18.79 | -18.90 | 2025-02-19 | 2025-04-08 |

### Nikkei 225

| Year | Start | End | Return(%) | 📈 Up Days | 📉 Down Days | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | 10654.79 | 10228.92 | -4.00 | 121 | 121 | -0.24 | 21.03 | -22.18 | 2010-04-05 | 2010-08-31 |
| 2011 | 10398.10 | 8455.35 | -18.68 | 123 | 121 | -0.92 | 23.48 | -24.84 | 2011-02-21 | 2011-11-25 |
| 2012 | 8560.11 | 10395.18 | 21.44 | 129 | 118 | 1.12 | 16.25 | -19.11 | 2012-03-27 | 2012-06-04 |
| 2013 | 10688.11 | 16291.31 | 52.42 | 136 | 108 | 1.64 | 26.86 | -20.36 | 2013-05-22 | 2013-06-13 |
| 2014 | 15908.88 | 17450.77 | 9.69 | 129 | 114 | 0.43 | 20.28 | -13.72 | 2014-01-08 | 2014-04-14 |
| 2015 | 17408.71 | 19033.71 | 9.33 | 139 | 104 | 0.40 | 21.20 | -18.87 | 2015-06-24 | 2015-09-29 |
| 2016 | 18450.98 | 19114.37 | 3.60 | 128 | 116 | 0.16 | 27.03 | -18.96 | 2016-01-04 | 2016-06-24 |
| 2017 | 19594.16 | 22764.94 | 16.18 | 128 | 118 | 1.12 | 11.66 | -6.61 | 2017-03-13 | 2017-04-14 |
| 2018 | 23506.33 | 20014.77 | -14.85 | 127 | 117 | -0.93 | 19.00 | -21.07 | 2018-10-02 | 2018-12-25 |
| 2019 | 19561.96 | 23656.62 | 20.93 | 135 | 105 | 1.31 | 13.66 | -9.17 | 2019-04-25 | 2019-08-26 |
| 2020 | 23204.86 | 27444.17 | 18.27 | 122 | 119 | 0.69 | 25.97 | -31.27 | 2020-01-20 | 2020-03-19 |
| 2021 | 27258.38 | 28791.71 | 5.63 | 125 | 119 | 0.24 | 18.63 | -11.34 | 2021-02-16 | 2021-08-20 |
| 2022 | 29301.79 | 26094.50 | -10.95 | 125 | 118 | -0.64 | 20.39 | -15.73 | 2022-01-05 | 2022-03-09 |
| 2023 | 25716.86 | 33464.17 | 30.13 | 142 | 103 | 1.58 | 16.02 | -9.56 | 2023-07-03 | 2023-10-04 |
| 2024 | 33288.29 | 39894.54 | 19.85 | 130 | 114 | 0.73 | 26.12 | -25.50 | 2024-07-11 | 2024-08-05 |
| 2025 | 39307.05 | 50339.48 | 28.07 | 134 | 108 | 1.07 | 23.91 | -22.32 | 2025-01-07 | 2025-04-07 |

### FTSE 100

| Year | Start | End | Return(%) | 📈 Up Days | 📉 Down Days | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | 5500.30 | 5899.90 | 7.27 | 131 | 121 | 0.32 | 17.40 | -17.50 | 2010-04-15 | 2010-07-01 |
| 2011 | 6013.90 | 5572.30 | -7.34 | 123 | 127 | -0.40 | 21.25 | -18.83 | 2011-02-08 | 2011-10-04 |
| 2012 | 5699.90 | 5897.80 | 3.47 | 126 | 123 | 0.10 | 13.85 | -11.82 | 2012-03-16 | 2012-06-01 |
| 2013 | 6027.40 | 6749.10 | 11.97 | 142 | 110 | 0.75 | 12.01 | -11.86 | 2013-05-22 | 2013-06-24 |
| 2014 | 6717.90 | 6566.10 | -2.26 | 132 | 119 | -0.41 | 11.37 | -10.12 | 2014-05-14 | 2014-12-15 |
| 2015 | 6547.80 | 6242.30 | -4.67 | 128 | 122 | -0.36 | 17.30 | -17.31 | 2015-04-27 | 2015-12-14 |
| 2016 | 6093.40 | 7142.80 | 17.22 | 138 | 114 | 0.86 | 16.68 | -9.78 | 2016-01-05 | 2016-02-11 |
| 2017 | 7177.90 | 7687.80 | 7.10 | 130 | 121 | 0.50 | 8.56 | -4.40 | 2017-06-02 | 2017-09-15 |
| 2018 | 7648.10 | 6728.10 | -12.03 | 126 | 126 | -1.18 | 12.71 | -16.41 | 2018-05-22 | 2018-12-27 |
| 2019 | 6734.20 | 7542.40 | 12.00 | 136 | 116 | 0.77 | 11.75 | -8.06 | 2019-07-29 | 2019-08-15 |
| 2020 | 7604.30 | 6460.50 | -15.04 | 132 | 120 | -0.51 | 29.36 | -34.93 | 2020-01-17 | 2020-03-23 |
| 2021 | 6571.90 | 7384.50 | 12.36 | 134 | 118 | 0.75 | 12.67 | -6.78 | 2021-01-08 | 2021-01-29 |
| 2022 | 7505.20 | 7451.70 | -0.71 | 135 | 113 | -0.15 | 16.40 | -11.03 | 2022-02-10 | 2022-10-12 |
| 2023 | 7554.10 | 7733.20 | 2.37 | 135 | 115 | 0.00 | 11.50 | -9.45 | 2023-02-20 | 2023-07-07 |
| 2024 | 7721.50 | 8173.00 | 5.85 | 132 | 121 | 0.33 | 9.41 | -5.18 | 2024-05-15 | 2024-08-05 |
| 2025 | 8260.10 | 9940.70 | 20.35 | 148 | 103 | 1.36 | 12.02 | -13.43 | 2025-03-03 | 2025-04-09 |

### KOSPI 200

| Year | Start | End | Return(%) | 📈 Up Days | 📉 Down Days | Sharpe | Vol(%) | Max DD(%) | DD Peak | DD Trough |
| :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| 2010 | 223.49 | 271.19 | 21.34 | 137 | 105 | 1.14 | 16.09 | -10.80 | 2010-04-26 | 2010-05-25 |
| 2011 | 273.81 | 238.08 | -13.05 | 116 | 121 | -0.50 | 28.09 | -27.48 | 2011-05-02 | 2011-09-26 |
| 2012 | 245.82 | 263.92 | 7.36 | 118 | 118 | 0.35 | 16.99 | -14.30 | 2012-04-03 | 2012-07-25 |
| 2013 | 269.16 | 264.24 | -1.83 | 112 | 123 | -0.29 | 13.93 | -13.98 | 2013-01-02 | 2013-06-26 |
| 2014 | 257.64 | 244.05 | -5.27 | 120 | 123 | -0.72 | 11.11 | -11.55 | 2014-07-30 | 2014-10-17 |
| 2015 | 244.79 | 240.38 | -1.80 | 126 | 119 | -0.31 | 12.97 | -18.73 | 2015-04-23 | 2015-08-24 |
| 2016 | 234.63 | 260.01 | 10.82 | 129 | 114 | 0.66 | 12.77 | -5.22 | 2016-01-05 | 2016-01-21 |
| 2017 | 262.97 | 324.74 | 23.49 | 136 | 100 | 1.91 | 10.47 | -5.99 | 2017-07-24 | 2017-08-11 |
| 2018 | 326.00 | 261.98 | -19.64 | 121 | 120 | -1.65 | 14.90 | -23.03 | 2018-01-29 | 2018-10-29 |
| 2019 | 258.23 | 293.77 | 13.76 | 134 | 110 | 0.83 | 13.49 | -13.29 | 2019-04-16 | 2019-08-07 |
| 2020 | 290.35 | 389.29 | 34.08 | 153 | 94 | 1.08 | 28.90 | -34.89 | 2020-01-22 | 2020-03-19 |
| 2021 | 399.88 | 394.19 | -1.42 | 124 | 123 | -0.17 | 17.31 | -15.25 | 2021-06-25 | 2021-11-30 |
| 2022 | 395.40 | 291.10 | -26.38 | 112 | 130 | -1.70 | 19.35 | -28.84 | 2022-01-04 | 2022-09-30 |
| 2023 | 289.79 | 357.99 | 23.53 | 127 | 117 | 1.28 | 15.72 | -12.95 | 2023-08-01 | 2023-10-31 |
| 2024 | 360.55 | 317.82 | -11.85 | 118 | 125 | -0.65 | 21.19 | -21.27 | 2024-07-11 | 2024-12-09 |
| 2025 | 317.77 | 605.98 | 90.70 | 150 | 90 | 2.87 | 23.42 | -14.26 | 2025-03-21 | 2025-04-09 |

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

### Index Benchmark Daily Data (`Index benchmark data/`)

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
