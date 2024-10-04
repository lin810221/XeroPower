import yfinance as yf

from indicators.price_alias import PriceAlias
from indicators.mad import MAD
from indicators.bollinger_bands import BollingerBands
from indicators.moving_average import MovingAverage
from analysis.technical_analysis import TechnicalAnalysis
from plot.plotter import Plotter

# 載入股票數據
ticker = '2308.TW'
start = '2024-01-01'
end = None
df = yf.download(ticker, start=start, end=end)
origin_df = df.copy()


days = 20
price_type = 'Close'

PriceAlias.calculate(df)
ta = TechnicalAnalysis(df)

MAD.calculate(df, days, price_type)
ta.analyze_MAD()

MovingAverage().calculate_SMA(df, days=days, price_type=price_type)
ta.analyze_SMA()

MovingAverage().calculate_EMA(df, days=days, price_type=price_type, adjust=True)
ta.analyze_EMA()

MovingAverage().calculate_WMA(df, days=days, price_type=price_type)
ta.analyze_WMA()

BollingerBands.calculate(df, days=days, num_std=2)
ta.analyze_Bollinger_Bands()

ta.analyze_MACD()

# df.to_csv('stock_data.csv', index=False)


# 繪製結果
Plotter.plot(df, 'SMA')
Plotter.plot(df, 'MACD')
Plotter.plot(df, 'Bollinger_Bands')
