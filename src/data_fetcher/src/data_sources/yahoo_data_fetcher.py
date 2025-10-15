from .base_data_fetcher import BaseDataFetcher
from ..securities.security import Security
import yfinance as yf
from datetime import datetime
from typing import List, Dict


class YahooDataFetcher(BaseDataFetcher):
    def __init__(self, securities: List[Security]):
        super().__init__(securities)
        self.tickers = {security.datasource_ticker: yf.Ticker(security.datasource_ticker) for security in securities}

    def get_prices(self, date: datetime) -> Dict[str, float]:
        return {security.datasource_ticker: self.tickers[security.datasource_ticker].history(start=date, end=date)['Close'].iloc[0] for security in self.securities}
        
    def get_price_history(self, start_date: datetime, end_date: datetime, frequency:int, price_type: str = "Close") -> List[float]:
        ticker_list = list(self.tickers.keys())
        return yf.download(tickers=ticker_list, start=start_date, end=end_date, interval=f"{frequency}d")[price_type]

    def get_return_history(self, start_date: datetime, end_date: datetime, frequency: str) -> List[float]:
        ticker_list = list(self.tickers.keys())
        return yf.download(tickers=ticker_list, start=start_date, end=end_date, interval=f"{frequency}d")