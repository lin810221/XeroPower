import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands

def download_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

def calculate_indicators(data, ma_days=50, ema_days=50, bb_std_dev=2):
    # 移動平均線 (MA) 和 指數平滑移動平均線 (EMA)
    data[f'MA{ma_days}'] = SMAIndicator(data['Close'], window=ma_days).sma_indicator()
    data[f'MA{ma_days*2}'] = SMAIndicator(data['Close'], window=ma_days*2).sma_indicator()
    data[f'EMA{ema_days}'] = EMAIndicator(data['Close'], window=ema_days).ema_indicator()
    data[f'EMA{ema_days*2}'] = EMAIndicator(data['Close'], window=ema_days*2).ema_indicator()


    # KD 指標
    stoch = StochasticOscillator(high=data['High'], low=data['Low'], close=data['Close'])
    data['K'] = stoch.stoch()
    data['D'] = stoch.stoch_signal()

    # MACD
    macd = MACD(data['Close'])
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()
    data['MACD_Hist'] = macd.macd_diff()

    # 布林通道
    bollinger = BollingerBands(data['Close'], window_dev=bb_std_dev)
    data['BB_High'] = bollinger.bollinger_hband()
    data['BB_Low'] = bollinger.bollinger_lband()
    data['BB_Mid'] = bollinger.bollinger_mavg()

    # 相對強弱指數 (RSI)
    data['RSI'] = RSIIndicator(data['Close']).rsi()

    # 標準差
    data['STD'] = data['Close'].rolling(window=20).std()

    # ADX 指標
    adx = ADXIndicator(high=data['High'], low=data['Low'], close=data['Close'])
    data['ADX'] = adx.adx()
    
    # 斐波那契回調
    high_price = data['High'].max()
    low_price = data['Low'].min()
    diff = high_price - low_price
    data['Fibonacci_23.6'] = high_price - (diff * 0.236)
    data['Fibonacci_38.2'] = high_price - (diff * 0.382)
    data['Fibonacci_50.0'] = high_price - (diff * 0.5)
    data['Fibonacci_61.8'] = high_price - (diff * 0.618)
    data['Fibonacci_100.0'] = low_price

def generate_signals(data, ma_days=50, ema_days=50):
    # 移動平均線 (MA) 買賣點
    data['MA_Signal'] = np.where(data[f'MA{ma_days}'] > data[f'MA{ma_days*2}'], 1, -1)

    # EMA 買賣點
    data['EMA_Signal'] = np.where(data[f'EMA{ema_days}'] > data[f'EMA{ema_days*2}'], 1, -1)

    # KD 指標買賣點
    data['KD_Signal'] = np.where(data['K'] > data['D'], 1, -1)

    # MACD 買賣點
    data['MACD_Signal'] = np.where(data['MACD'] > data['MACD_Signal'], 1, -1)

    # RSI 買賣點
    data['RSI_Signal'] = np.where(data['RSI'] < 30, 1, np.where(data['RSI'] > 70, -1, 0))

    # 布林通道買賣點
    data['BB_Signal'] = np.where(data['Close'] < data['BB_Low'], 1, np.where(data['Close'] > data['BB_High'], -1, 0))

    # 合併所有信號
    data['Signal'] = data[['MA_Signal', 'EMA_Signal', 'KD_Signal', 'MACD_Signal', 'RSI_Signal', 'BB_Signal']].mean(axis=1)
    data['Buy_Sell'] = np.where(data['Signal'] > 0, 'Buy', np.where(data['Signal'] < 0, 'Sell', 'Hold'))


def plot_data(data, ticker, ma_days=50, ema_days=50):
    fig, axes = plt.subplots(8, 1, figsize=(14, 36))
    fig.suptitle(f'Stock Analysis for {ticker}', fontsize=18)
    
    # 調整圖形與標題之間的間距
    plt.subplots_adjust(top=0.95, hspace=0.3)

    # 收盤價及移動平均線
    axes[0].plot(data['Close'], label='Close')
    axes[0].plot(data[f'MA{ma_days}'], label=f'MA{ma_days}')
    axes[0].plot(data[f'MA{ma_days*2}'], label=f'MA{ma_days*2}')
    axes[0].set_title('Close Price and Moving Averages')
    axes[0].legend()

    # MACD
    axes[1].plot(data['MACD'], label='MACD')
    axes[1].plot(data['MACD_Signal'], label='Signal')
    axes[1].bar(data.index, data['MACD_Hist'], label='Histogram', color='gray')
    axes[1].set_title('MACD')
    axes[1].legend()

    # RSI
    axes[2].plot(data['RSI'], label='RSI')
    axes[2].axhline(70, color='red', linestyle='--')
    axes[2].axhline(30, color='green', linestyle='--')
    axes[2].set_title('RSI')
    axes[2].legend()

    # 布林通道
    axes[3].plot(data['Close'], label='Close')
    axes[3].plot(data['BB_High'], label='Bollinger High')
    axes[3].plot(data['BB_Low'], label='Bollinger Low')
    axes[3].plot(data['BB_Mid'], label='Bollinger Mid')
    axes[3].set_title('Bollinger Bands')
    axes[3].legend()
    
    # KD 指標
    axes[4].plot(data['K'], label='K')
    axes[4].plot(data['D'], label='D')
    axes[4].axhline(80, color='red', linestyle='--')
    axes[4].axhline(20, color='green', linestyle='--')
    axes[4].set_title('KD Indicator')
    axes[4].legend()

    # ADX
    axes[5].plot(data['ADX'], label='ADX')
    axes[5].set_title('ADX')
    axes[5].legend()

    # 斐波那契回調
    axes[6].plot(data['Close'], label='Close')
    axes[6].axhline(data['Fibonacci_23.6'][0], color='red', linestyle='--', label='Fibonacci 23.6%')
    axes[6].axhline(data['Fibonacci_38.2'][0], color='orange', linestyle='--', label='Fibonacci 38.2%')
    axes[6].axhline(data['Fibonacci_50.0'][0], color='yellow', linestyle='--', label='Fibonacci 50.0%')
    axes[6].axhline(data['Fibonacci_61.8'][0], color='green', linestyle='--', label='Fibonacci 61.8%')
    axes[6].axhline(data['Fibonacci_100.0'][0], color='blue', linestyle='--', label='Fibonacci 100.0%')
    axes[6].set_title('Fibonacci Retracement')
    axes[6].legend()
    
    # 標準差
    axes[7].plot(data['STD'], label='Standard Deviation')
    axes[7].set_title('Standard Deviation')
    axes[7].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.98])  # 調整布局，確保標題不重疊
    plt.show()