import mplfinance as mpf
from matplotlib.lines import Line2D

class Plotter:
    @staticmethod
    def plot(df, indicator, style='binance'):
        # 設置mplfinance的圖表風格
        mpf_style = mpf.make_mpf_style(
            base_mpf_style=style,
            marketcolors=mpf.make_marketcolors(up='r', down='g', inherit=True)
        )
        
        # 通用設置參數
        kwargs = dict(type='candle', volume=True, figratio=(15, 8), style=mpf_style)
        
        # 添加買賣信號圖
        def add_signals(df, buy_col, sell_col):
            # 獲取買賣信號
            buy_signals = df['Close'].where(df[buy_col] == 1)
            sell_signals = df['Close'].where(df[sell_col] == -1)
            ap_buy = mpf.make_addplot(buy_signals, type='scatter', markersize=50, marker='^', color='green')
            ap_sell = mpf.make_addplot(sell_signals, type='scatter', markersize=50, marker='v', color='red')
            return [ap_buy, ap_sell]


        # 根據不同技術指標設置不同圖表
        if indicator == 'SMA':
            kwargs.update({
                'title': 'SMA Analysis',
                'mav': (20, 60),
                'addplot': add_signals(df, 'SMA_Position', 'SMA_Position')
            })

        
        elif indicator == 'MACD':
            ap_macd = mpf.make_addplot(df['MACD'], panel=1, color='blue')
            ap_signal = mpf.make_addplot(df['MACD_Signal'], panel=1, color='red')
            kwargs.update({
                'title': 'MACD Analysis',
                'addplot': [ap_macd, ap_signal] + add_signals(df, 'MACD_Position', 'MACD_Position'),
                'panel_ratios': (2, 1)
            })
            
            
        elif indicator == 'Bollinger_Bands':
            ap_upper = mpf.make_addplot(df['Upper_Band'], color='blue')
            ap_lower = mpf.make_addplot(df['Lower_Band'], color='red')
            kwargs.update({
                'title': 'Bollinger Bands Analysis',
                'addplot': [ap_upper, ap_lower] + add_signals(df, 'Bollinger_Bands_Position', 'Bollinger_Bands_Position')
            })
        
        elif indicator == 'RSI':
            ap_rsi = mpf.make_addplot(df['RSI'], panel=1, color='purple')  # 顯示RSI指標
            kwargs.update({
                'title': 'RSI Analysis',
                'addplot': [ap_rsi] + add_signals(df, 'RSI_Position', 'RSI_Position')
            })
       
        elif indicator == 'RSV':
            ap_rsv = mpf.make_addplot(df['RSV'], panel=2, color='green')  # 顯示Raw Stochastic Value指標
            kwargs.update({
                'title': 'Raw Stochastic Value Analysis',
                'addplot': [ap_rsv] + add_signals(df, 'RSV_Position', 'RSV_Position'),
                'panel_ratios': (2, 1)
            })

            '''
        elif indicator == 'Raw_Stochastic':
            ap_stochastic = mpf.make_addplot(df['Raw_Stochastic'], panel=1, color='orange')
            kwargs.update({
                'title': 'Raw Stochastic Value Analysis',
                'addplot': [ap_stochastic] + Plotter.add_signals(df, 'Raw_Stochastic_Position', 'Raw_Stochastic_Position'),
                'panel_ratios': (2, 1)
            })
            '''          
        
        elif indicator == 'Raw_Stochastic':
            ap_k = mpf.make_addplot(df['K'], panel=2, color='orange')  # 顯示K值
            ap_d = mpf.make_addplot(df['D'], panel=2, color='red')     # 顯示D值
            kwargs.update({
                'title': 'Raw Stochastic Analysis',
                'addplot': [ap_k, ap_d] + add_signals(df, 'Raw_Stochastic_Position', 'Raw_Stochastic_Position')
            })

        elif indicator == 'WPR':
            ap_wpr = mpf.make_addplot(df['Williams_%R'], panel=1, color='cyan')
            kwargs.update({
                'title': 'Williams %R Analysis',
                'addplot': [ap_wpr] + add_signals(df, 'Williams_%R_Position', 'Williams_%R_Position'),
                'panel_ratios': (2, 1)
            })

        elif indicator == 'CCI':
            ap_cci = mpf.make_addplot(df['CCI'], panel=1, color='brown')
            kwargs.update({
                'title': 'Commodity Channel Index Analysis',
                'addplot': [ap_cci] + add_signals(df, 'CCI_Position', 'CCI_Position'),
                'panel_ratios': (2, 1)
            })

        elif indicator == 'ATR':
            ap_atr = mpf.make_addplot(df['ATR'], panel=1, color='magenta')
            kwargs.update({
                'title': 'Average True Range Analysis',
                'addplot': [ap_atr] + add_signals(df, 'ATR_Position', 'ATR_Position'),
                'panel_ratios': (2, 1)
            })

        
        else:
            raise ValueError(f"不支援的技術指標: {indicator}")
        
        # 繪製圖表
        fig, axlist = mpf.plot(df, **kwargs, returnfig=True)
        ax = axlist[0]
        
        # 設定圖例
        legend_elements = [
            Line2D([0], [0], marker='^', color='w', markerfacecolor='green', markersize=10, label='Buy Signal'),
            Line2D([0], [0], marker='v', color='w', markerfacecolor='red', markersize=10, label='Sell Signal')
        ]
        
        # 添加圖例
        ax.legend(handles=legend_elements, loc='best')
        
        # 顯示圖表
        mpf.show()
