from .base_data_fetcher import BaseDataFetcher
from .nasdaq_data_fetcher import NasdaqDataFetcher
from .yahoo_data_fetcher import YahooDataFetcher
from ..securities.security import Security
from typing import List

class DataFetcherFactory:
    def __init__(self, securities: List[Security]):
        self.securities = securities

    def fetcher(self):

        if self.data_source == "nasdaq":
            return NasdaqDataFetcher(self.security)
        elif self.data_source == "yahoo":
            return YahooDataFetcher(self.security)
        else:
            raise ValueError(f"Data source {self.data_source} not supported")