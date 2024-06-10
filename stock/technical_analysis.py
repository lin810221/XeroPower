import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands

def download_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

def calculate_indicators(data):
    # 移動平均線 (MA) 和 指數平滑移動平均線 (EMA)
    data['MA50'] = SMAIndicator(data['Close'], window=50).sma_indicator()
    data['MA200'] = SMAIndicator(data['Close'], window=200).sma_indicator()
    data['EMA50'] = EMAIndicator(data['Close'], window=50).ema_indicator()
    data['EMA200'] = EMAIndicator(data['Close'], window=200).ema_indicator()

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
    bollinger = BollingerBands(data['Close'])
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

def generate_signals(data):
    # 移動平均線 (MA) 買賣點
    data['MA_Signal'] = np.where(data['MA50'] > data['MA200'], 1, -1)

    # EMA 買賣點
    data['EMA_Signal'] = np.where(data['EMA50'] > data['EMA200'], 1, -1)

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

def plot_data(data):
    fig, axes = plt.subplots(5, 1, figsize=(14, 24))

    # 收盤價及移動平均線
    axes[0].plot(data['Close'], label='Close')
    axes[0].plot(data['MA50'], label='MA50')
    axes[0].plot(data['MA200'], label='MA200')
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

    # ADX
    axes[4].plot(data['ADX'], label='ADX')
    axes[4].set_title('ADX')
    axes[4].legend()

    plt.tight_layout()
    plt.show()


