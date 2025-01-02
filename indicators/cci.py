class CCI:
    @staticmethod
    def calculate(df, period=20, constant=0.015):
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        sma = typical_price.rolling(window=period).mean()
        mean_deviation = typical_price.rolling(window=period).apply(lambda x: (abs(x - x.mean())).mean())
        df['CCI'] = (typical_price - sma) / (constant * mean_deviation)
        return df
