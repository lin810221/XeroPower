import yfinance as yf

# from indicators.price_alias import PriceAlias
# from indicators.mad import MAD
# from indicators.bollinger_bands import BollingerBands
# from indicators.moving_average import MovingAverage
# from indicators.rsi import RSI
# from indicators.raw_stochastic import RSV, RawStochastic
# from indicators.williams_percent_range import WilliamsPercentRange
# from indicators.cci import CCI
# from indicators.atr import ATR
from analysis.technical_analysis import TechnicalAnalysis
from plot.plotter import Plotter

# 載入股票數據
ticker = '3231.TW'
start = '2024-01-01'
end = None
df = yf.download(ticker, start=start, end=end)
origin_df = df.copy()


days = 20
price_type = 'Close'

# 各種典型價碼指標
# PriceAlias.calculate(df)
ta = TechnicalAnalysis(df)

# Mean Absolute Deviation (MAD)
# MAD.calculate(df, days, price_type)
ta.analyze_MAD()

# Simple Moving Average (SMA)
# MovingAverage().calculate_SMA(df, days=days, price_type=price_type)
ta.analyze_SMA()

# Exponential Moving Average (EMA)
# MovingAverage().calculate_EMA(df, days=days, price_type=price_type, adjust=True)
ta.analyze_EMA()

# Weighted Moving Average (WMA)
# MovingAverage().calculate_WMA(df, days=days, price_type=price_type)
ta.analyze_WMA()

# Bollingers Bands
# BollingerBands.calculate(df, days=days, num_std=2)
ta.analyze_Bollinger_Bands()

# Moving Average Convergence Divergence (MACD)
ta.analyze_MACD()

# Relative Strength Index (RSI)
# RSI.calculate(df, price_type=price_type)
ta.analyze_RSI()

# Raw Stochastic Value (RSV)
# RSV.calculate(df, price_type=price_type)
ta.analyze_RSV()


# Stochastic Oscillator (KD)
# RawStochastic.calculate(df, price_type=price_type)
ta.analyze_Raw_Stochastic()

# The Williams Percent Range (W%R)
# WilliamsPercentRange.calculate(df, price_type=price_type)
ta.analyze_Williams_Percentage_Range()

# Commodity Channel Index (CCI)
# CCI.calculate(df)
ta.analyze_CCI()

# Average True Range (ATR)
# ATR.calculate(df, price_type=price_type)
ta.analyze_ATR()






# df.to_csv('stock_data.csv', index=False)


# 繪製結果
Plotter.plot(df, 'SMA')
Plotter.plot(df, 'MACD')
Plotter.plot(df, 'Bollinger_Bands')
Plotter.plot(df, 'RSI')
Plotter.plot(df, 'RSV')
Plotter.plot(df, 'Raw_Stochastic')
Plotter.plot(df, 'WPR')
Plotter.plot(df, 'CCI')
Plotter.plot(df, 'ATR')

















































