import numpy as np

class MovingAverage:
    # 計算 Simple Moving Average (SMA)
    @staticmethod
    def calculate_SMA(df, days=20, price_type='Close'):
        df[f'MA_{days}'] = df[price_type].rolling(window=days).mean()
        return df
    
    # 計算 Exponential Moving Average (EMA)
    @staticmethod
    def calculate_EMA(df, days=20, price_type='Close', adjust=True):
        df[f'EMA_{days}'] = df[price_type].ewm(span=days, adjust=adjust).mean()
        return df

    # 計算 Weighted Moving Average (WMA)
    @staticmethod
    def calculate_WMA(df, days=20, price_type='Close'):
        weights = np.arange(1, days + 1)
        df[f'WMA_{days}'] = df[price_type].rolling(window=days).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
        return df
