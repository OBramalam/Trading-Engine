import pandas as pd
import numpy as np

from ..indicators import Indicators as indicators

class Signals:
    
    @staticmethod
    def ma_crossover(data: pd.Series, short: int, long: int, ma_type: str = "sma") -> pd.Series:
        
        if ma_type == "sma":
            short_ma = indicators.sma(data, 30)
            long_ma = indicators.sma(data, 200)
        elif ma_type == "ema":
            short_ma = indicators.ema(data, 30)
            long_ma = indicators.ema(data, 200)
        else:
            raise ValueError(rf"{ma_type} is not a supported type of moving average for this signal")

        signal = np.where(short_ma > long_ma, 1, -1)
        
        return signal