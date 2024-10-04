from indicators.moving_average import MovingAverage
from indicators.mad import MAD
from indicators.macd import MACD
from indicators.bollinger_bands import BollingerBands
from signals.signal_generator import SignalGenerator


class TechnicalAnalysis:
    def __init__(self, df):
        self.df = df

    def analyze_SMA(self, short_days=20, long_days=60):
        MovingAverage.calculate_SMA(self.df, short_days)
        MovingAverage.calculate_SMA(self.df, long_days)
        buy_condition = self.df[f'MA_{short_days}'] > self.df[f'MA_{long_days}']
        sell_condition = self.df[f'MA_{short_days}'] < self.df[f'MA_{long_days}']
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'SMA')

    def analyze_EMA(self, short_days=12, long_days=26):
        MovingAverage.calculate_EMA(self.df, short_days)
        MovingAverage.calculate_EMA(self.df, long_days)
        buy_condition = self.df[f'EMA_{short_days}'] > self.df[f'EMA_{long_days}']
        sell_condition = self.df[f'EMA_{short_days}'] < self.df[f'EMA_{long_days}']
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'EMA')

    def analyze_WMA(self, days=20):
        MovingAverage.calculate_WMA(self.df, days)
        buy_condition = self.df[f'WMA_{days}'] > self.df[f'WMA_{days}'].shift(1)
        sell_condition = self.df[f'WMA_{days}'] < self.df[f'WMA_{days}'].shift(1)
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'WMA')

    def analyze_MAD(self, days=20):
        MAD.calculate(self.df, days)
        buy_condition = self.df[f'MAD_{days}'] < self.df[f'MAD_{days}'].mean()
        sell_condition = self.df[f'MAD_{days}'] > self.df[f'MAD_{days}'].mean()
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'MAD')

    def analyze_Bollinger_Bands(self, days=20, num_std=2):
        BollingerBands.calculate(self.df, days, num_std)
        buy_condition = self.df['Close'] < self.df['Lower_Band']
        sell_condition = self.df['Close'] > self.df['Upper_Band']
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'Bollinger_Bands')

    def analyze_MACD(self, short_days=12, long_days=26, signal_days=9):
        MACD.calculate(self.df, short_days, long_days, signal_days)
        buy_condition = self.df['MACD'] > self.df['MACD_Signal']
        sell_condition = self.df['MACD'] < self.df['MACD_Signal']
        return SignalGenerator.generate_signal(self.df, buy_condition, sell_condition, 'MACD')






