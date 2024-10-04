import stock.data_fetcher
import stock.technical_analysis

stock_fetcher = stock.data_fetcher.StockDataFetcher()
df = stock_fetcher.get_data()

# 主程式
ticker = '2308.TW'
start = '2023-01-01'
end = None
data = stock.technical_analysis.download_data(ticker, start=start, end=end)

# 設定參數
ma_days = 50
ema_days = 50
bb_std_dev = 2

# 計算指標
stock.technical_analysis.calculate_indicators(data, ma_days=ma_days, ema_days=ema_days, bb_std_dev=bb_std_dev)
stock.technical_analysis.generate_signals(data, ma_days=ma_days, ema_days=ema_days)
stock.technical_analysis.plot_data(data, ticker, ma_days=ma_days, ema_days=ema_days)

# 顯示買賣點
buy_signals = data[data['Buy_Sell'] == 'Buy']
sell_signals = data[data['Buy_Sell'] == 'Sell']

print("Buy Signals:")
print(buy_signals[['Close', 'Buy_Sell']].iloc[-1])

print("Sell Signals:")
print(sell_signals[['Close', 'Buy_Sell']].iloc[-1])

# 顯示個別指標的最新一天買賣建議和價位
latest_data = data.iloc[-1]
indicators = ['MA_Signal', 'EMA_Signal', 'KD_Signal', 'MACD_Signal', 'RSI_Signal', 'BB_Signal']
for indicator in indicators:
    signal = latest_data[indicator]
    close_price = latest_data['Close']
    action = "Buy" if signal == 1 else "Sell" if signal == -1 else "Hold"
    print(f"{indicator} Signal on {latest_data.name}: {action} at price {close_price}")
