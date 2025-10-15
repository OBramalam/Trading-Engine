import pandas as pd
import numpy as np

from ..indicators import Indicators as indicators

class Signals:
    
    @staticmethod
    def ma_crossover(data: pd.DataFrame, short: int, long: int, ma_type: str = "sma") -> pd.Series:
        
        close_prices = data['Close']

        if ma_type == "sma":
            short_ma = indicators.sma(close_prices, short)
            long_ma = indicators.sma(close_prices, long)
        elif ma_type == "ema":
            short_ma = indicators.ema(close_prices, short)
            long_ma = indicators.ema(close_prices, long)
        else:
            raise ValueError(rf"{ma_type} is not a supported type of moving average for this signal")

        signal = (short_ma > long_ma).astype(int) * 2 - 1
        
        return signal

    @staticmethod
    def atr_strategy(data: pd.DataFrame, atr_period: int, atr_support_multiplier: float, n_day_high: int) -> pd.Series:
        
        atr = indicators.atr(data['High'], data['Low'], atr_period)
        n_day_high = data['High'].rolling(window=n_day_high).max()
        atr_support = n_day_high - (atr_support_multiplier * atr)
        prev_high = data['High'].shift(1)

        signal = pd.Series(0, index=data.index)

        signal[data['Close'] < atr_support] = 1
        signal[data['Close'] > prev_high] = -1

        return signal

