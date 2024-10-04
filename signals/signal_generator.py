class SignalGenerator:
    @staticmethod
    def generate_signal(df, buy_condition, sell_condition, indicator_name):
        df[f'{indicator_name}_Signal'] = 0
        df.loc[buy_condition, f'{indicator_name}_Signal'] = 1
        df.loc[sell_condition, f'{indicator_name}_Signal'] = -1
        df[f'{indicator_name}_Signal'] = df[f'{indicator_name}_Signal'].where(df[f'{indicator_name}_Signal'].diff().abs() <= 1, 0)
        df[f'{indicator_name}_Position'] = df[f'{indicator_name}_Signal'].diff().fillna(0)
        df[f'{indicator_name}_Advice'] = 'Hold'
        df.loc[df[f'{indicator_name}_Position'] == 1, f'{indicator_name}_Advice'] = 'Buy'
        df.loc[df[f'{indicator_name}_Position'] == -1, f'{indicator_name}_Advice'] = 'Sell'
        return df
