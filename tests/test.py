import yfinance as yf
import mplfinance as mpf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D



class TechnicalIndicators:
    def __init__(self, df):
        self.df = df

    # 計算價格類型（Alias）
    def calculate_price_alias(self):
        # Typical Price (HLC3)
        self.df['typical_price'] = (self.df['High'] + self.df['Low'] + self.df['Close']) / 3
        
        # Median Price (HL2)
        self.df['median_price'] = (self.df['High'] + self.df['Low']) / 2
        
        # Weighted Price (OHLC4)
        self.df['weighted_price'] = (self.df['Open'] + self.df['High'] + self.df['Low'] + self.df['Close']) / 4
        
        # Weighted Close Price (HLCC4)
        self.df['weighted_close_price'] = (self.df['High'] + self.df['Low'] + self.df['Close'] + self.df['Close']) / 4
        
        return self.df
    
    # 計算 Simple Moving Average (SMA)
    def calculate_SMA(self, days = 20, price_type = 'Close'):
        self.df[f'MA_{days}'] = self.df[price_type].rolling(window=days).mean()
        return self.df
    
    # 計算 Exponential Moving Average (EMA)
    def calculate_EMA(self, days=20, price_type='Close'):
        self.df[f'EMA_{days}'] = self.df[price_type].ewm(span=days, adjust=True).mean()
        return self.df

    # 計算 Weighted Moving Average (WMA)
    def calculate_WMA(self, days=20, price_type='Close'):
        weights = np.arange(1, days + 1)
        wma = self.df[price_type].rolling(window=days).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
        self.df[f'WMA_{days}'] = wma
        return self.df

    # 計算 Mean Absolute Deviation (MAD)
    def calculate_MAD(self, days=20, price_type='Close'):
        mad = self.df[price_type].rolling(window=days).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
        self.df[f'MAD_{days}'] = mad
        return self.df




class TechnicalAnalysis(TechnicalIndicators):
    def generate_signal(self, buy_condition, sell_condition, indicator_name):
        """根據指標條件生成買賣信號"""
        self.df[f'{indicator_name}_Signal'] = 0  # 初始化信號列
        
        # 生成买入信号
        self.df.loc[buy_condition, f'{indicator_name}_Signal'] = 1
        
        # 生成卖出信号
        self.df.loc[sell_condition, f'{indicator_name}_Signal'] = -1

        # 清理重复信号，防止出现 2 或 -2
        self.df[f'{indicator_name}_Signal'] = self.df[f'{indicator_name}_Signal'].where(self.df[f'{indicator_name}_Signal'].diff().abs() <= 1, 0)

        # 計算買賣操作提示
        self.df[f'{indicator_name}_Position'] = self.df[f'{indicator_name}_Signal'].diff().fillna(0)
        
        # 生成操作建议
        self.df[f'{indicator_name}_Advice'] = 'Hold'
        self.df.loc[self.df[f'{indicator_name}_Position'] == 1, f'{indicator_name}_Advice'] = 'Buy'
        self.df.loc[self.df[f'{indicator_name}_Position'] == -1, f'{indicator_name}_Advice'] = 'Sell'
        
        return self.df

    def analyze_SMA(self, short_days=20, long_days=60):
        """使用短期和長期SMA進行買賣信號分析"""
        self.calculate_SMA(days=short_days)
        self.calculate_SMA(days=long_days)
        
        # 黃金交叉（買入）與死亡交叉（賣出）
        buy_condition = self.df[f'MA_{short_days}'] > self.df[f'MA_{long_days}']
        sell_condition = self.df[f'MA_{short_days}'] < self.df[f'MA_{long_days}']
        
        return self.generate_signal(buy_condition, sell_condition, 'SMA')

    def analyze_EMA(self, short_days=12, long_days=26, signal_days=9):
        """使用EMA和MACD進行買賣信號分析"""
        self.calculate_EMA(days=short_days)
        self.calculate_EMA(days=long_days)
        
        self.df['MACD'] = self.df[f'EMA_{short_days}'] - self.df[f'EMA_{long_days}']
        self.df['Signal_Line'] = self.df['MACD'].ewm(span=signal_days, adjust=False).mean()
        
        buy_condition = self.df['MACD'] > self.df['Signal_Line']
        sell_condition = self.df['MACD'] < self.df['Signal_Line']
        
        return self.generate_signal(buy_condition, sell_condition, 'MACD')

    def analyze_Bollinger_Bands(self, days=20, num_std=2):
        """使用布林通道進行分析"""
        self.calculate_SMA(days=days)
        
        self.df['Upper_Band'] = self.df[f'MA_{days}'] + num_std * self.df['Close'].rolling(window=days).std()
        self.df['Lower_Band'] = self.df[f'MA_{days}'] - num_std * self.df['Close'].rolling(window=days).std()
        
        buy_condition = self.df['Close'] < self.df['Lower_Band']
        sell_condition = self.df['Close'] > self.df['Upper_Band']

        return self.generate_signal(buy_condition, sell_condition, 'Bollinger_Bands')

    # 發出訊息（買賣點）
    def __str__(self):
        signals = []
        for col in self.df.columns:
            if '_Advice' in col:
                advice_points = self.df[self.df[col] != 'Hold'][[col, 'Close']]
                signals.append(f"\n{col}:\n{advice_points.to_string()}")
        return '\n'.join(signals)

    # 繪製多個技術分析的個別圖表
    def draw_plot(self, indicators, base_mpf_style='binance'):
        style = mpf.make_mpf_style(
            base_mpf_style=base_mpf_style,
            marketcolors=mpf.make_marketcolors(up='r', down='g', inherit=True)
        )
        
        # 針對每個技術指標單獨繪製圖表
        for indicator in indicators:
            if indicator == 'SMA':
                # 獲取 SMA 的買賣信號
                buy_signals = self.df['Close'].where(self.df['SMA_Position'] == 1)
                sell_signals = self.df['Close'].where(self.df['SMA_Position'] == -1)
                
                # 設定買賣點的圖形元素
                ap_buy = mpf.make_addplot(buy_signals, type='scatter', markersize=50, marker='^', color='forestgreen')
                ap_sell = mpf.make_addplot(sell_signals, type='scatter', markersize=50, marker='v', color='firebrick')
                
                # 繪製包含 SMA 的圖表
                kwargs = dict(
                    type='candle', mav=(20, 60), volume=True, figratio=(15, 8),
                    title='SMA Analysis', style=style, addplot=[ap_buy, ap_sell]
                )
                
            elif indicator == 'MACD':
                # 獲取 MACD 的買賣信號
                buy_signals = self.df['Close'].where(self.df['MACD_Position'] == 1)
                sell_signals = self.df['Close'].where(self.df['MACD_Position'] == -1)
    
                # 設定 MACD 買賣信號的圖形元素
                ap_buy = mpf.make_addplot(buy_signals, type='scatter', markersize=50, marker='^', color='forestgreen')
                ap_sell = mpf.make_addplot(sell_signals, type='scatter', markersize=50, marker='v', color='firebrick')
    
                # 顯示 MACD 和 Signal Line
                ap_macd = mpf.make_addplot(self.df['MACD'], panel=1, color='b')
                ap_signal = mpf.make_addplot(self.df['Signal_Line'], panel=1, color='r')
    
                # 繪製包含 MACD 的圖表
                kwargs = dict(
                    type='candle', volume=True, figratio=(15, 8), addplot=[ap_macd, ap_signal, ap_buy, ap_sell],
                    title='MACD Analysis', style=style, panel_ratios=(2,1)
                )
    
            elif indicator == 'Bollinger_Bands':
                # 獲取 Bollinger Bands 的買賣信號
                buy_signals = self.df['Close'].where(self.df['Bollinger_Bands_Position'] == 1)
                sell_signals = self.df['Close'].where(self.df['Bollinger_Bands_Position'] == -1)
    
                # 設定買賣點的圖形元素
                ap_buy = mpf.make_addplot(buy_signals, type='scatter', markersize=50, marker='^', color='forestgreen')
                ap_sell = mpf.make_addplot(sell_signals, type='scatter', markersize=50, marker='v', color='firebrick')
    
                # 顯示 Bollinger Bands 的上軌和下軌
                ap_upper = mpf.make_addplot(self.df['Upper_Band'], color='blue')
                ap_lower = mpf.make_addplot(self.df['Lower_Band'], color='blue')
    
                # 繪製包含 Bollinger Bands 的圖表
                kwargs = dict(
                    type='candle', volume=True, figratio=(15, 8), addplot=[ap_upper, ap_lower, ap_buy, ap_sell],
                    title='Bollinger Bands Analysis', style=style
                )
    
            # 繪製圖表
            fig, axlist = mpf.plot(self.df, **kwargs, returnfig=True)
            ax = axlist[0]
    
            # 根據指標設定圖例
            legend_elements = [
                Line2D([0], [0], marker='^', color='w', markerfacecolor='forestgreen', markersize=10, label='Buy Signal'),
                Line2D([0], [0], marker='v', color='w', markerfacecolor='firebrick', markersize=10, label='Sell Signal')
            ]
    
            # 添加圖例
            ax.legend(handles=legend_elements, loc='best')
    
            # 顯示圖表
            plt.show()









ticker = '2308.TW'
start = '2024-01-01'
end = None
df = yf.download(ticker, start=start, end=end)
origin_df = df.copy()


# =============================================================================
# 創建技術分析物件並計算指標
# =============================================================================
# 初始化技術分析
ta = TechnicalAnalysis(df)
ta.calculate_price_alias()
ta.calculate_SMA()
ta.calculate_EMA()
ta.calculate_WMA()
ta.calculate_MAD()

# SMA 分析
ta.analyze_SMA(short_days=20, long_days=60)

# EMA 和 MACD 分析
ta.analyze_EMA(short_days=12, long_days=26, signal_days=9)

# 布林通道分析
ta.analyze_Bollinger_Bands(days=20, num_std=2)

# 顯示分析結果
print(ta.df.tail())

# 打印買賣訊號
print(ta)




# 使用多個技術指標進行分析
analysis = TechnicalAnalysis(df)
analysis.analyze_SMA(short_days=20, long_days=60)
analysis.analyze_EMA(short_days=12, long_days=26, signal_days=9)
analysis.analyze_Bollinger_Bands(days=20)

# 繪製三張圖表，分別針對每個技術指標
indicators = ['SMA', 'MACD', 'Bollinger_Bands']
analysis.draw_plot(indicators=indicators)

df.to_csv('STOCK.csv', index=False)






# 根據黃金交叉和死亡交叉給出買、賣、持有提示
def generate_signals(df = df):
    # 初始化信號列
    df['Signal'] = 0  
    
    # 當20日均線上穿60日均線，產生買入信號
    df.loc[df['MA_20'] > df['MA_60'], 'Signal'] = 1
    
    # 當20日均線下穿60日均線，產生賣出信號
    df.loc[df['MA_20'] < df['MA_60'], 'Signal'] = -1

    # 如果信號是從1直接變到-1，或從-1直接變到1，我們將它設置為0
    df['Signal'] = df['Signal'].where(df['Signal'].diff().abs() <= 1, 0)

    # 提取信號，將信號變化轉換為買入/賣出操作
    df['Position'] = df['Signal'].diff()

    # 根據Position生成提示
    df['Advice'] = 'Hold'
    df.loc[df['Position'] == 1, 'Advice'] = 'Buy'  # 黃金交叉，提示買入
    df.loc[df['Position'] == -1, 'Advice'] = 'Sell'  # 死亡交叉，提示賣出
    
    return df


def draw_plot(base_mpf_style = 'binance', title = 'stock'):
    
    # 風格配置
    style  = mpf.make_mpf_style(base_mpf_style = base_mpf_style, 
                                marketcolors = mpf.make_marketcolors(up = 'r', down = 'g', inherit = True),
                                )
    
    # 確保買賣信號與df的大小匹配，並為沒有信號的日期填充 NaN
    buy_signals = df['Close'].where(df['Position'] == 1)
    sell_signals = df['Close'].where(df['Position'] == -1)
    
    # 用於標記買入信號的點
    ap_buy = mpf.make_addplot(buy_signals, type='scatter', markersize = 50, marker = '^', color = 'forestgreen')
    
    # 用於標記賣出信號的點
    ap_sell = mpf.make_addplot(sell_signals, type='scatter', markersize = 50, marker = 'v', color = 'firebrick')

    # 設定移動平均線顏色與圖例顏色一致
    mav_colors = ['cyan', 'magenta']
    
    kwargs = dict(type='candle', mav = (20, 60), volume = True, figratio = (15, 8),
                  title = f'Candlestick Chart for {ticker}', style = style, 
                  addplot = [ap_buy, ap_sell], mavcolors = mav_colors)

    # 畫出 mplfinance 圖表
    fig, axlist = mpf.plot(df, **kwargs, returnfig = True)

    # 添加 legend
    ax = axlist[0]  # 獲取主圖
    # 自定義圖例項目
    legend_elements = [
        Line2D([0], [0], color = 'cyan', lw = 1, label = '20-Day MA'),  # 20日均線
        Line2D([0], [0], color = 'magenta', lw = 1, label = '60-Day MA'),  # 60日均線
        Line2D([0], [0], marker = '^', color = 'w', markerfacecolor = 'forestgreen', markersize = 10, label = 'Buy Signal'),  # 買入信號
        Line2D([0], [0], marker = 'v', color = 'w', markerfacecolor = 'firebrick', markersize = 10, label = 'Sell Signal')   # 賣出信號
    ]

    # 添加圖例到圖表上
    ax.legend(handles=legend_elements, loc='best')

    plt.show()



# =============================================================================
# 前置處理
# =============================================================================
# df = Alias(df)

# =============================================================================
# SMA
# =============================================================================
# 計算短期和長期移動平均線


# =============================================================================
# EMA
# =============================================================================

# =============================================================================
# WMA
# =============================================================================





















'''
styles = mpf.available_styles()

for style in styles:
    draw_plot(base_mpf_style = style, title = style)
'''




'''
# 將日期設為索引
df.index = pd.to_datetime(df.index)

# 整理資料以適合K棒繪製
df = df.reset_index()
df['Date'] = mdates.date2num(df['Date']).astype(datetime.date)  # 將日期轉換為 matplotlib 數值日期
# mdates.date2num(df['Date'].astype(dt.date))
# 設置圖表
fig, ax = plt.subplots(figsize=(12, 6))

# 繪製K棒圖
ohlc_data = df[['Date', 'Open', 'High', 'Low', 'Close']].values
candlestick_ohlc(ax, ohlc_data, width=0.8, colorup='red', colordown='green')

# 設定日期格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
ax.grid(True)

# 設置標題
plt.title(f'Candlestick Chart for {ticker}', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Price')

# 顯示圖表
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# SMA
from ta.trend import SMAIndicator

# 計算 SMA
sma = SMAIndicator(df['Close'], window=20).sma_indicator()
df['SMA'] = sma

# 繪製 SMA 圖
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Close'], label='Close')
plt.plot(df.index, df['SMA'], label='SMA')
plt.title('Simple Moving Average (SMA)')
plt.legend()
plt.show()

'''




