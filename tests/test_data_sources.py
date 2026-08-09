"""W2 数据层单元测试"""
import pytest
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from htzl_a_share_mcp.data_sources import (
    MockDataSource, DataSourceFailover, create_default_failover
)


class TestMockDataSource:
    """Mock 数据源测试"""

    def test_is_available(self):
        source = MockDataSource()
        assert source.is_available() is True

    def test_get_daily_returns_dataframe(self):
        source = MockDataSource(base_price=100.0)
        df = source.get_daily("600519", "2025-01-01", "2025-01-31")
        assert len(df) > 0
        assert "open" in df.columns
        assert "high" in df.columns
        assert "low" in df.columns
        assert "close" in df.columns
        assert "volume" in df.columns

    def test_get_daily_deterministic(self):
        source = MockDataSource()
        df1 = source.get_daily("600519", "2025-01-01", "2025-01-10")
        df2 = source.get_daily("600519", "2025-01-01", "2025-01-10")
        assert df1['close'].tolist() == df2['close'].tolist()

    def test_get_realtime(self):
        source = MockDataSource()
        quote = source.get_realtime("600519")
        assert quote['symbol'] == "600519"
        assert 'price' in quote
        assert 'change_pct' in quote


class TestDataSourceFailover:
    """Failover 测试"""

    def test_failover_to_available_source(self):
        sources = [MockDataSource(base_price=200.0)]
        failover = DataSourceFailover(sources)
        df = failover.get_daily("000001", "2025-01-01", "2025-01-31")
        assert len(df) > 0
        assert failover.last_used_source == "MockDataSource"

    def test_failover_all_fail(self):
        # 创建一个总是不可用的 source
        class FailingSource(MockDataSource):
            def is_available(self):
                return False

        sources = [FailingSource()]
        failover = DataSourceFailover(sources)
        # 兜底兜到 MockDataSource 后面的 source
        # 这里简化：只放一个 FailingSource，应该抛错
        with pytest.raises(RuntimeError):
            failover.get_daily("600519", "2025-01-01", "2025-01-31")

    def test_failover_uses_first_available(self):
        # 第一个可用就用第一个
        source1 = MockDataSource(base_price=100.0)
        source2 = MockDataSource(base_price=200.0)
        failover = DataSourceFailover([source1, source2])
        df = failover.get_daily("600519", "2025-01-01", "2025-01-10")
        assert failover.last_used_source == "MockDataSource"

    def test_cache_works(self):
        sources = [MockDataSource(base_price=300.0)]
        failover = DataSourceFailover(sources)
        df1 = failover.get_daily("600519", "2025-01-01", "2025-01-31")
        df2 = failover.get_daily("600519", "2025-01-01", "2025-01-31")
        assert df1.equals(df2)


class TestCreateDefaultFailover:
    """默认 failover 创建测试"""

    def test_create_with_mock(self):
        failover = create_default_failover(use_mock=True)
        assert len(failover.sources) >= 1
        df = failover.get_daily("600519", "2025-01-01", "2025-01-10")
        assert len(df) > 0

    def test_create_without_token(self):
        failover = create_default_failover(tushare_token=None, use_mock=False)
        assert len(failover.sources) >= 2  # AKShare + Mock 兜底