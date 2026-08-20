"""
tools/concept_tools.py — 题材/概念板块类工具（参考 tradex astock_signals/concept.py）

W7+ 增量：当前 4 个 stub (concept / dragon_tiger / northbound / hot_money)
完整实现需 R856+（避免今晚超时）
"""
import os
from datetime import datetime
from ..data_sources import create_default_failover
from .registry import register_tool


_failover = None


def _get_failover():
    global _failover
    if _failover is None:
        use_mock = os.getenv("HTZL_USE_MOCK", "true").lower() == "true"
        tushare_token = os.getenv("TUSHARE_TOKEN")
        _failover = create_default_failover(
            tushare_token=tushare_token,
            use_mock=use_mock,
            enable_baostock=True,
        )
    return _failover


# === 工具实现（stub + 装饰器双轨制）===

@register_tool("L1-题材板块", "获取概念板块列表（东财 push2delay）")
def get_concept_board(symbol: str = None) -> list:
    """获取概念板块列表（东财 push2delay）

    Args:
        symbol: 股票代码（可选），返回该股票所属概念板块

    Returns:
        概念板块列表
    """
    return [
        {"code": "BK0001", "name": "AI算力", "change_pct": 1.23, "leader": "300750"},
        {"code": "BK0002", "name": "新能源车", "change_pct": -0.45, "leader": "002594"},
        {"code": "BK0003", "name": "白酒", "change_pct": 0.12, "leader": "600519"},
        {"code": "BK0004", "name": "半导体", "change_pct": 2.34, "leader": "688981"},
        {"code": "BK0005", "name": "医药", "change_pct": -1.23, "leader": "600276"},
    ]


@register_tool("L1-龙虎榜", "获取龙虎榜（东财 datacenter）")
def get_dragon_tiger_board(date: str = None) -> list:
    """获取龙虎榜（东财 datacenter）

    Args:
        date: 日期 YYYY-MM-DD，默认最近交易日

    Returns:
        龙虎榜明细
    """
    return [
        {
            "symbol": "600519",
            "name": "贵州茅台",
            "net_buy": 12345678,
            "buy_seats": ["机构专用", "招商益田路"],
            "sell_seats": ["东方杭州龙井"],
        }
    ]


@register_tool("L1-北向资金", "获取北向资金流向（沪深股通）")
def get_northbound_flow(days: int = 30) -> list:
    """获取北向资金流向（沪深股通）

    Args:
        days: 查询天数（默认 30）

    Returns:
        北向资金日流向数据
    """
    return [
        {"date": "2026-08-19", "sh_net": 12.34, "sz_net": -5.67, "total_net": 6.67},
        {"date": "2026-08-18", "sh_net": 8.12, "sz_net": 3.45, "total_net": 11.57},
    ]


@register_tool("L1-游资", "获取游资/热门资金追踪")
def get_hot_money(date: str = None) -> list:
    """获取游资/热门资金追踪

    Args:
        date: 日期 YYYY-MM-DD，默认最近交易日

    Returns:
        游资席位追踪数据
    """
    return [
        {
            "symbol": "300750",
            "name": "宁德时代",
            "hot_money_seats": ["拉萨团结路", "上海溧阳路"],
            "total_buy": 56789012,
        }
    ]


# === 注册接口（tradex register(mcp) 风格）===

def register(mcp):
    """注册到 mcp 实例"""
    mcp.tool()(get_concept_board)
    mcp.tool()(get_dragon_tiger_board)
    mcp.tool()(get_northbound_flow)
    mcp.tool()(get_hot_money)
    return ["get_concept_board", "get_dragon_tiger_board", "get_northbound_flow", "get_hot_money"]
