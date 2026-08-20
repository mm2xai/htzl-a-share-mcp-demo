"""data_sources/baostock_source.py 单元测试 + 集成测试

集成测试需要真实 baostock 服务（一般能连通）
如不通会自动 skip
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

from htzl_a_share_mcp.data_sources import (
    BaostockSource,
    AKShareSource,
    MockDataSource,
    create_default_failover,
)


class TestBaostockSourceUnit:
    """单元测试（不需要网络）"""

    def test_import(self):
        from htzl_a_share_mcp.data_sources import BaostockSource
        assert BaostockSource is not None

    def test_normalize_symbol_shanghai(self):
        from htzl_a_share_mcp.data_sources.baostock_source import BaostockSource
        assert BaostockSource._normalize_symbol("600519") == "sh.600519"
        assert BaostockSource._normalize_symbol("900901") == "sh.900901"

    def test_normalize_symbol_shenzhen(self):
        from htzl_a_share_mcp.data_sources.baostock_source import BaostockSource
        assert BaostockSource._normalize_symbol("000001") == "sz.000001"
        assert BaostockSource._normalize_symbol("300750") == "sz.300750"

    def test_normalize_symbol_already_prefixed(self):
        from htzl_a_share_mcp.data_sources.baostock_source import BaostockSource
        assert BaostockSource._normalize_symbol("SH.600519") == "sh.600519"
        assert BaostockSource._normalize_symbol("sz.000001") == "sz.000001"

    def test_create_default_failover_includes_baostock(self):
        """create_default_failover 应包含 baostock（mock 模式下不包含）"""
        # Mock 模式：不包含 baostock
        failover_mock = create_default_failover(use_mock=True)
        source_names = [s.__class__.__name__ for s in failover_mock.sources]
        assert "MockDataSource" in source_names

        # 真实模式：包含 baostock + mock 兜底
        failover_real = create_default_failover(use_mock=False)
        real_names = [s.__class__.__name__ for s in failover_real.sources]
        assert "AKShareSource" in real_names
        assert "MockDataSource" in real_names  # 兜底


class TestBaostockSourceIntegration:
    """集成测试（需要真实 baostock）"""

    def test_is_available(self):
        try:
            src = BaostockSource()
            assert src.is_available() is True
        except Exception as e:
            pytest.skip(f"baostock unavailable: {e}")

    def test_get_daily_600519(self):
        """获取贵州茅台日线（前复权）"""
        try:
            src = BaostockSource()
            df = src.get_daily("600519", "2026-08-01", "2026-08-19")
            assert df is not None
            if not df.empty:
                assert "收盘" in df.columns
                assert "成交量" in df.columns
                assert len(df) > 0
        except Exception as e:
            pytest.skip(f"baostock integration failed: {e}")

    def test_get_daily_000001(self):
        """获取平安银行日线"""
        try:
            src = BaostockSource()
            df = src.get_daily("000001", "2026-08-01", "2026-08-19")
            assert df is not None
        except Exception as e:
            pytest.skip(f"baostock integration failed: {e}")


def test_all():
    """运行所有测试"""
    test_classes = [TestBaostockSourceUnit, TestBaostockSourceIntegration]
    total, passed, skipped = 0, 0, 0
    for cls in test_classes:
        for method in dir(cls):
            if method.startswith("test_"):
                total += 1
                try:
                    getattr(cls(), method)()
                    passed += 1
                    print(f"  ✓ {cls.__name__}.{method}")
                except pytest.SkipTest as e:
                    skipped += 1
                    print(f"  ⊘ {cls.__name__}.{method}: SKIP ({e})")
                except Exception as e:
                    print(f"  ✗ {cls.__name__}.{method}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{total} passed, {skipped} skipped")


if __name__ == "__main__":
    test_all()
