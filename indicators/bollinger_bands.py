from .moving_average import MovingAverage

class BollingerBands:
    @staticmethod
    def calculate(df, days=20, num_std=2):
        MovingAverage.calculate_SMA(df, days)
        df['Upper_Band'] = df[f'MA_{days}'] + num_std * df['Close'].rolling(window=days).std()
        df['Lower_Band'] = df[f'MA_{days}'] - num_std * df['Close'].rolling(window=days).std()
        return df
