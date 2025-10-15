from ..securities.security import Security
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

class BaseDataFetcher(ABC):
    def __init__(self, securities: List[Security]):
        self.securities = securities


    