import stock.data_fetcher

stock_fetcher = stock.data_fetcher.StockDataFetcher()
df = stock_fetcher.get_data()
