"""tools/registry.py 单元测试"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from htzl_a_share_mcp.tools.registry import (
    ToolRegistry, ToolMeta, register_tool, register,
)


class TestToolRegistry:
    """ToolRegistry 测试"""

    def setup_method(self):
        """每个测试前清空"""
        from htzl_a_share_mcp.tools.registry import _get_registry
        _get_registry().clear()

    def test_register_tool_decorator(self):
        @register_tool("L1-数据获取", "搜索A股股票")
        async def search_stock(keyword: str) -> str:
            return f"found {keyword}"

        tools = ToolRegistry.get_all()
        assert "search_stock" in tools
        meta = tools["search_stock"]
        assert meta.category == "L1-数据获取"
        assert "搜索A股股票" in meta.description

    def test_get_by_category(self):
        @register_tool("L1-数据获取", "A")
        def tool_a(x: str) -> str: return x

        @register_tool("L2-计算引擎", "B")
        def tool_b(x: int) -> int: return x

        @register_tool("L1-数据获取", "C")
        def tool_c(x: float) -> float: return x

        l1 = ToolRegistry.get_by_category("L1-数据获取")
        l2 = ToolRegistry.get_by_category("L2-计算引擎")
        assert len(l1) == 2
        assert len(l2) == 1

    def test_stats(self):
        from htzl_a_share_mcp.tools.registry import _get_registry
        _get_registry().clear()  # 清前面测试残留

        @register_tool("L1", "x")
        def f1(): pass

        @register_tool("L2", "y")
        def f2(): pass

        stats = ToolRegistry.stats()
        assert stats["total"] == 2
        assert stats["by_category"]["L1"] == 1
        assert stats["by_category"]["L2"] == 1

    def test_auto_discover(self):
        import importlib
        tools_pkg = importlib.import_module("htzl_a_share_mcp.tools")
        discovered = ToolRegistry.auto_discover(tools_pkg)
        # 至少有 data_tools.py
        assert discovered >= 1

    def test_register_to_mcp(self):
        """register_to_mcp 应能挂到 FastMCP 实例"""
        from fastmcp import FastMCP
        mcp = FastMCP("test")

        @register_tool("L1-测试", "测试工具")
        def sample_tool(x: int) -> int:
            return x * 2

        names = ToolRegistry.register_all(mcp)
        assert "sample_tool" in names

    def test_register_tradex_style(self):
        """register(mcp) tradex 兼容接口"""
        from fastmcp import FastMCP
        mcp = FastMCP("test2")
        names = register(mcp)
        assert isinstance(names, list)


def test_all():
    test_classes = [TestToolRegistry]
    total, passed = 0, 0
    for cls in test_classes:
        for method in dir(cls):
            if method.startswith("test_"):
                total += 1
                try:
                    getattr(cls(), method)()
                    passed += 1
                    print(f"  ✓ {cls.__name__}.{method}")
                except Exception as e:
                    traceback.print_exc()
                    print(f"  ✗ {cls.__name__}.{method}: {e}")
    print(f"\n{passed}/{total} tests passed")
    assert passed == total


if __name__ == "__main__":
    test_all()
