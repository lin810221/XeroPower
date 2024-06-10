import stock.data_fetcher
import stock.technical_analysis

stock_fetcher = stock.data_fetcher.StockDataFetcher()
df = stock_fetcher.get_data()


# 主程式
ticker = '2330.TW'  # 台積電的股票代碼
data = stock.technical_analysis.download_data(ticker, start='2020-01-01', end='2023-01-01')
stock.technical_analysis.calculate_indicators(data)
stock.technical_analysis.generate_signals(data)
stock.technical_analysis.plot_data(data)

# 顯示買賣點
buy_signals = data[data['Buy_Sell'] == 'Buy']
sell_signals = data[data['Buy_Sell'] == 'Sell']

print("Buy Signals:")
print(buy_signals[['Close', 'Buy_Sell']])

print("Sell Signals:")
print(sell_signals[['Close', 'Buy_Sell']])