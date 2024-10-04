import numpy as np

class MAD:
    # 計算 Mean Absolute Deviation (MAD)
    @staticmethod
    def calculate(df, days=20, price_type='Close'):
        df[f'MAD_{days}'] = df[price_type].rolling(window=days).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
        return df