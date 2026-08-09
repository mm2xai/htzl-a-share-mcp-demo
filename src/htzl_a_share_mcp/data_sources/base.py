"""数据源抽象基类"""
from abc import ABC, abstractmethod
import pandas as pd


class BaseDataSource(ABC):
    """数据源抽象基类"""

    @abstractmethod
    def get_daily(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """获取日线数据"""
        pass

    @abstractmethod
    def get_realtime(self, symbol: str) -> dict:
        """获取实时行情"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        pass