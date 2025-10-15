from .get_price_history import get_price_history
from typing import List
from ..securities.security import Security
from datetime import datetime
import pandas as pd


def get_return_history(securities: List[Security], start_date: datetime, end_date: datetime) -> pd.DataFrame:
    price_history = get_price_history(securities, start_date, end_date)
    return_history = price_history.pct_change()
    return_history.dropna(inplace=True)
    return return_history