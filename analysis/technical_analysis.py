from indicators.moving_average import MovingAverage
from indicators.mad import MAD
from indicators.macd import MACD
from indicators.bollinger_bands import BollingerBands
from indicators.rsi import RSI
from indicators.raw_stochastic import RSV, RawStochastic
from indicators.williams_percent_range import WilliamsPercentRange
from indicators.cci import CCI
from indicators.atr import ATR
from signals.signal_generator import SignalGenerator


class TechnicalAnalysis:
    def __init__(self, df, price_type='Close'):
        self.df = df
        self.price_type = price_type

    def analyze_SMA(self, short_days=20, long_days=60):
        MovingAverage.calculate_SMA(self.df, short_days, self.price_type)
        MovingAverage.calculate_SMA(self.df, long_days, self.price_type)
        buy_condition = self.df[f'MA_{short_days}'] > self.df[f'MA_{long_days}']
        sell_condition = self.df[f'MA_{short_days}'] < self.df[f'MA_{long_days}']
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'SMA')

    def analyze_EMA(self, short_days=12, long_days=26):
        MovingAverage.calculate_EMA(self.df, short_days, self.price_type)
        MovingAverage.calculate_EMA(self.df, long_days, self.price_type)
        buy_condition = self.df[f'EMA_{short_days}'] > self.df[f'EMA_{long_days}']
        sell_condition = self.df[f'EMA_{short_days}'] < self.df[f'EMA_{long_days}']
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'EMA')

    def analyze_WMA(self, days=20):
        MovingAverage.calculate_WMA(self.df, days)
        buy_condition = self.df[f'WMA_{days}'] > self.df[f'WMA_{days}'].shift(1)
        sell_condition = self.df[f'WMA_{days}'] < self.df[f'WMA_{days}'].shift(1)
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'WMA')

    def analyze_MAD(self, days=20):
        MAD.calculate(self.df, days, self.price_type)
        buy_condition = self.df[f'MAD_{days}'] < self.df[f'MAD_{days}'].mean()
        sell_condition = self.df[f'MAD_{days}'] > self.df[f'MAD_{days}'].mean()
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'MAD')

    def analyze_Bollinger_Bands(self, days=20, num_std=2):
        BollingerBands.calculate(self.df, days, num_std)
        buy_condition = self.df['Close'] < self.df['Lower_Band']
        sell_condition = self.df['Close'] > self.df['Upper_Band']
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'Bollinger_Bands')

    def analyze_MACD(self, short_days=12, long_days=26, signal_days=9):
        MACD.calculate(self.df, short_days, long_days, signal_days, self.price_type)
        buy_condition = self.df['MACD'] > self.df['MACD_Signal']
        sell_condition = self.df['MACD'] < self.df['MACD_Signal']
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'MACD')

    def analyze_RSI(self, period=14):
        RSI.calculate(self.df, period, self.price_type)
        buy_condition = self.df['RSI'] < 30  # 超賣
        sell_condition = self.df['RSI'] > 70  # 超買
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'RSI')

    def analyze_RSV(self, period=14):
        RSV.calculate(self.df, period, self.price_type)
        buy_condition = self.df['RSV'] < 20  # 超賣
        sell_condition = self.df['RSV'] > 80  # 超買
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'RSV')

    def analyze_Raw_Stochastic(self, k_period=14, d_period=3):
        RawStochastic.calculate(self.df, k_period, d_period, self.price_type)
        buy_condition = self.df['K'] > self.df['D']  # 黃金交叉
        sell_condition = self.df['K'] < self.df['D']  # 死亡交叉
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'Raw_Stochastic')


    def analyze_Williams_Percentage_Range(self, period=14):
        WilliamsPercentRange.calculate(self.df, period, self.price_type)
        buy_condition = self.df['Williams_%R'] < -80  # 超賣
        sell_condition = self.df['Williams_%R'] > -20  # 超買
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'Williams_%R')

    def analyze_CCI(self, period=20):
        CCI.calculate(self.df, period)
        buy_condition = self.df['CCI'] < -100  # 超賣
        sell_condition = self.df['CCI'] > 100  # 超買
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'CCI')

    def analyze_ATR(self, period=14):
        ATR.calculate(self.df, period, self.price_type)
        # ATR 通常用來判斷波動率，這裡不設明確買賣點，但可以依照策略設定
        # return self.df  # 這裡的例子不產生買賣訊號，僅計算 ATR
        buy_condition = self.df['ATR'] > self.df['ATR'].shift(1)  # ATR 增加
        sell_condition = self.df['ATR'] < self.df['ATR'].shift(1)  # ATR 減少
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'ATR')






