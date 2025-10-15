
import pandas as pd
from typing import List
from ..securities.security_serializer import SecuritySerializer
from ..data_sources.yahoo_data_fetcher import YahooDataFetcher
from datetime import datetime
from ..securities.security import Security


def get_price_history(securities: List[Security], start_date: datetime, end_date: datetime, price_type: str = "Close") -> pd.DataFrame:
    data_fetcher = YahooDataFetcher(securities)
    return data_fetcher.get_price_history(start_date, end_date, 1, price_type)
