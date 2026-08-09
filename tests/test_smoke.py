"""Smoke test - 验证模块导入"""

def test_import():
    """基础导入测试"""
    from htzl_a_share_mcp import __version__
    assert __version__ == "0.1.0"


def test_strategies_import():
    """策略模块导入"""
    from htzl_a_share_mcp.strategies import TurtleStrategy, ChanlunStrategy, MultiFactorStrategy
    assert TurtleStrategy is not None
    assert ChanlunStrategy is not None
    assert MultiFactorStrategy is not None


def test_data_sources_import():
    """数据源模块导入"""
    from htzl_a_share_mcp.data_sources import AKShareSource, TushareSource, DataSourceFailover
    assert AKShareSource is not None
    assert TushareSource is not None
    assert DataSourceFailover is not None