class WilliamsPercentRange:
    @staticmethod
    def calculate(df, period=14, price_type='Close'):
        df['Highest_High'] = df['High'].rolling(window=period).max()
        df['Lowest_Low'] = df['Low'].rolling(window=period).min()
        df['Williams_%R'] = -100 * ((df['Highest_High'] - df['Close']) / (df['Highest_High'] - df['Lowest_Low']))
        return df
