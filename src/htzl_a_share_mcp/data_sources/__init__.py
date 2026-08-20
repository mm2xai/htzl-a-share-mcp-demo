"""数据源模块"""

from .base import BaseDataSource
from .akshare_source import AKShareSource
from .tushare_source import TushareSource
from .baostock_source import BaostockSource
from .mock_source import MockDataSource
from .failover import DataSourceFailover


def create_default_failover(
    tushare_token: str = None,
    use_mock: bool = False,
    enable_baostock: bool = True,
) -> DataSourceFailover:
    """创建默认数据源 failover (L1-L3 梯队)

    Args:
        tushare_token: Tushare Pro token
        use_mock: 是否使用 Mock 数据源（用于离线开发/测试）
        enable_baostock: 是否启用 Baostock 降级（默认 True）

    Source梯队（R852 起）:
        L1: AKShare（首选，数据全）
        L1: Baostock（akshare 失败时降级，老牌稳定）
        L2: Tushare（可选，需要 token）
        L3: MockDataSource（兜底，永远可用）
    """
    sources = []
    if use_mock:
        sources.append(MockDataSource())
    else:
        sources.append(AKShareSource())
        if enable_baostock:
            try:
                sources.append(BaostockSource())
            except ImportError:
                pass
        if tushare_token:
            sources.append(TushareSource(tushare_token))
    sources.append(MockDataSource(base_price=100.0))  # 兜底
    return DataSourceFailover(sources)


__all__ = [
    "BaseDataSource",
    "AKShareSource",
    "TushareSource",
    "BaostockSource",
    "MockDataSource",
    "DataSourceFailover",
    "create_default_failover",
]
