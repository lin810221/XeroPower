``` Bash
stock_analysis_project/
│
├── indicators/                 # 技術指標的邏輯
│   ├── __init__.py             # 模組初始化
│   ├── moving_averages.py      # 包含 SMA、EMA、WMA 邏輯
│   ├── bollinger_bands.py      # 布林通道邏輯
│   ├── mad.py                  # Mean Absolute Deviation 邏輯
│   ├── macd.py                 # Moving Average Convergence Divergence 邏輯
│   ├── price_alias.py          # 價格相關指標計算
│
├── analysis/                   # 買賣信號生成的邏輯
│   ├── __init__.py             # 模組初始化
│   ├── technical_analysis.py   # 根據技術指標進行分析
│
├── signals/                    # 買賣信號生成的邏輯
│   ├── __init__.py             # 模組初始化
│   ├── signal_generator.py     # 根據技術指標生成信號
│
├── plot/                       # 繪圖模組
│   ├── __init__.py             # 模組初始化
│   ├── plotter.py              # 繪製技術指標圖表
│
├── tests/                      # 測試模組
│   ├── __init__.py             # 模組初始化
│   ├── test_indicators.py      # 測試指標計算
│   ├── test_signals.py         # 測試信號生成
│   ├── test_plotting.py        # 測試繪圖功能
│
├── utils/                      # 共用工具與函數
│   ├── __init__.py             # 模組初始化
│   ├── data_loader.py          # 加載股票數據
│   ├── decorators.py           # 共用裝飾器
│
├── config/                     # 配置與常量
│   ├── __init__.py             # 模組初始化
│   ├── constants.py            # 常量定義
│
├── main.py                     # 主程式，管理整個分析流程
├── README.md                   # 專案說明文件
└── requirements.txt            # 依賴包清單
```
