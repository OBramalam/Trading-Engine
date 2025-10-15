import pandas as pd


class Indicators:

    @staticmethod
    def sma(data: pd.Series, window: int) -> pd.Series:
        sma = data.rolling(window=window).mean()
        return sma

    @staticmethod
    def ema(data: pd.Series, window: int) -> pd.Series:
        ema = data.ewm(span=window, adjust=False).mean()
        return ema