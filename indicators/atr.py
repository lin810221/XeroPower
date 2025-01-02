class ATR:
    @staticmethod
    def calculate(df, period=14, price_type='Close'):
        high_low = df['High'] - df['Low']
        high_close = (df['High'] - df[price_type].shift()).abs()
        low_close = (df['Low'] - df[price_type].shift()).abs()
        tr = high_low.combine(high_close, max).combine(low_close, max)
        df['ATR'] = tr.rolling(window=period).mean()
        return df
