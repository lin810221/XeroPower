class RSV:
    @staticmethod
    def calculate(df, period=14, price_type='Close'):
        """
        計算 Raw Stochastic Value (RSV)
        RSV = (當前收盤價 - 最近 N 天的最低價) / (最近 N 天的最高價 - 最近 N 天的最低價) * 100
        """
        df['Lowest_Low'] = df['Low'].rolling(window=period).min()
        df['Highest_High'] = df['High'].rolling(window=period).max()
        df['RSV'] = (df[price_type] - df['Lowest_Low']) / (df['Highest_High'] - df['Lowest_Low']) * 100
        

class RawStochastic:
    @staticmethod
    def calculate(df, k_period=14, d_period=3, price_type='Close'):
        """
        計算 Raw Stochastic (K 和 D 值)
        K = RSV 的移動平均
        D = K 的移動平均
        """
        RSV.calculate(df, k_period, price_type)  # 先計算 RSV
        df['K'] = df['RSV'].rolling(window=k_period).mean()  # 計算 K 值
        df['D'] = df['K'].rolling(window=d_period).mean()  # 計算 D 值
        
