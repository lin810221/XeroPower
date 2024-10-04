class MACD:
    @staticmethod
    def calculate(df, short_days=12, long_days=26, signal_days=9, price_type='Close'):
        # 計算短期和長期的EMA
        df['EMA_short'] = df[price_type].ewm(span=short_days, adjust=False).mean()
        df['EMA_long'] = df[price_type].ewm(span=long_days, adjust=False).mean()

        # 計算MACD線 (短期EMA - 長期EMA)
        df['MACD'] = df['EMA_short'] - df['EMA_long']

        # 計算信號線 (MACD的9天EMA)
        df['MACD_Signal'] = df['MACD'].ewm(span=signal_days, adjust=False).mean()

        # 生成買賣訊號的欄位：當 MACD 線 高於 訊號線 為買入，低於為賣出
        df['MACD_Position'] = 0
        df.loc[df['MACD'] > df['MACD_Signal'], 'MACD_Position'] = 1
        df.loc[df['MACD'] < df['MACD_Signal'], 'MACD_Position'] = -1

        return df