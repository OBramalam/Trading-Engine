import nasdaqdatalink as nasdaq
from .base_data_fetcher import BaseDataFetcher
from ..securities.security import Security
import os

class NasdaqDataFetcher(BaseDataFetcher):
    def __init__(self, security: Security):
        self.security = security

        nasdaq.ApiConfig.api_key = os.environ['NASDAQ_DATA_LINK_API_KEY']
        nasdaq.ApiConfig.verify_ssl = True

        self._session = nasdaq


    # def get_price_history(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    #     case table:
    #         case "Stocks":
    #             table = 'SHARADAR/SEP'
    #         case "Fund":
    #             table = 'SHARADAR/SFP'

    
    #     return nasdaq.get_table(table, ticker=self.security.datasource_ticker, start_date=start_date, end_date=end_date)


    # def get_tickers(self, table: str) -> pd.DataFrame:

    #     case table:
    #         case "Stocks":
    #             table = 'SHARADAR/SEP'
    #         case "Fund":
    #             table = 'SHARADAR/SFP'

    #     tickers = self._session.get_table("SHARADAR/TICKERS", paginate=True)



    #     'SFP', 'SF1', 'SEP'