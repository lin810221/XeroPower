import requests
import pandas as pd


class StockDataFetcher:
    # 臺灣證券交易所 OpenAPI: https://openapi.twse.com.tw/
    # 證券櫃檯買賣中心 OpenAPI: https://www.tpex.org.tw/openapi/
    # 臺灣集中保管結算所 OpenAPI: https://openapi.tdcc.com.tw/swagger-ui/index.html?configUrl=/tdcc-opendata-api-docs/swagger-config
    
    def __init__(self):
        # 定義不同交易所的資料端點、欄位對應以及分類
        self.endpoints = [
            ('https://openapi.twse.com.tw/v1/opendata/t187ap03_L', {'公司代號': '公司代號', '公司名稱': '公司名稱', '公司簡稱': '公司簡稱', '產業別': '產業別'}, '上市'),
            ('https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O', {'公司代號': 'SecuritiesCompanyCode', '公司名稱': 'CompanyName', '公司簡稱': '公司簡稱', '產業別': 'SecuritiesIndustryCode'}, '上櫃'),
            ('https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_R', {'公司代號': 'SecuritiesCompanyCode', '公司名稱': 'CompanyName', '公司簡稱': '公司簡稱', '產業別': 'SecuritiesIndustryCode'}, '興櫃'),
        ]

    def api_get(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return []

    def fetch_data(self, endpoint, column_mapping, category):
        data = self.api_get(endpoint)
        return [{column: entry.get(mapping) for column, mapping in column_mapping.items()} for entry in data]

    def get_data(self):
        df_list = [pd.DataFrame(self.fetch_data(endpoint, column_mapping, category), columns=['公司代號', '公司名稱', '公司簡稱', '產業別']).assign(分類=category) for endpoint, column_mapping, category in self.endpoints]
        df = pd.concat(df_list, ignore_index=True)
        df.set_index('公司代號', inplace=True)
        return df
    
    def save_to_csv(self, df, filename='output.csv'):
        df.to_csv(filename, sep = ',', index = True, header = True, encoding='utf-8-sig')
