"""数据源模块"""

from .base import BaseDataSource
from .akshare_source import AKShareSource
from .tushare_source import TushareSource
from .mock_source import MockDataSource
from .failover import DataSourceFailover


def create_default_failover(tushare_token: str = None, use_mock: bool = False) -> DataSourceFailover:
    """创建默认数据源 failover

    Args:
        tushare_token: Tushare Pro token
        use_mock: 是否使用 Mock 数据源（用于离线开发/测试）
    """
    sources = []
    if use_mock:
        sources.append(MockDataSource())
    else:
        sources.append(AKShareSource())
        if tushare_token:
            sources.append(TushareSource(tushare_token))
    sources.append(MockDataSource(base_price=100.0))  # 兜底
    return DataSourceFailover(sources)


__all__ = ["BaseDataSource", "AKShareSource", "TushareSource", "MockDataSource", "DataSourceFailover", "create_default_failover"]