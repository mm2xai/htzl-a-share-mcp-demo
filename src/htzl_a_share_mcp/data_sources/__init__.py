"""数据源模块"""

from .base import BaseDataSource
from .akshare_source import AKShareSource
from .tushare_source import TushareSource
from .failover import DataSourceFailover


def create_default_failover(tushare_token: str = None) -> DataSourceFailover:
    """创建默认二源 failover（akshare 优先 + tushare 备份）"""
    return DataSourceFailover([
        AKShareSource(),
        TushareSource(tushare_token or ""),
    ])


__all__ = ["BaseDataSource", "AKShareSource", "TushareSource", "DataSourceFailover", "create_default_failover"]