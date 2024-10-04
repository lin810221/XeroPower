class PriceAlias:
    @staticmethod
    def calculate(df):
        # Typical Price (HLC3)
        df['typical_price'] = (df['High'] + df['Low'] + df['Close']) / 3
        
        # Median Price (HL2)
        df['median_price'] = (df['High'] + df['Low']) / 2
        
        # Weighted Price (OHLC4)
        df['weighted_price'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
        
        # Weighted Close Price (HLCC4)
        df['weighted_close_price'] = (df['High'] + df['Low'] + df['Close'] * 2) / 4
        
        return df
