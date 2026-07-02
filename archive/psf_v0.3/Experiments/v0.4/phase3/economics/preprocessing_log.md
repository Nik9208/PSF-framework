# Preprocessing Log: Economics
**Date Generated:** 2026-07-02 14:18:21

## Representation Layer Separation Principle
Raw physical prices are archived. All inferences are conducted on Log-Returns to provide a stationary representation compatible with the ICCS metrics.

## Steps Executed:
1. Downloaded S&P 500 (^GSPC) via yfinance. Dates: 2000-01-01 to 2024-01-01.
2. Archived raw Adj Close prices.
3. Computed Log-Returns.
4. Generated FT Surrogate (Phase-randomized).
5. Generated IAAFT Surrogate (Amplitude Adjusted Fourier Transform).

## Summary:
- **Raw Price Days:** 6037
- **Log-Returns Length:** 6036
- **Raw Archive SHA256:** dbae7c4215b67819f4428ff5e664857313e451c0eef5101892b8caf31451de91
- **Log-Returns SHA256:** 59f4b787d58e47f7a763966fdefbe920820203d4997e97990d6ffb2281b52cd8
- **FT Surrogate SHA256:** 37580cc7e87ff2c2a633d1b55c61353aace55ed388f54d814400c6b56b4decb9
- **IAAFT Surrogate SHA256:** 2218f1d0a14a6cec333f77241e74f4e09b7397873922f8f34b6ad2256ac8593c
