"""
tools/data_tools.py — 数据获取类工具（L1）

参考 wolfjkd/tradex-hub tools/registry.py + 工具模块拆分模式
将原 server.py W5 5 个核心工具拆分到此
"""
from typing import Optional
from ..data_sources import create_default_failover
from ..utils.cache import get_cache, TTL_DAILY, TTL_REALTIME


# 全局 failover（模块级别单例）
_failover = None


def _get_failover():
    global _failover
    if _failover is None:
        import os
        use_mock = os.getenv("HTZL_USE_MOCK", "true").lower() == "true"
        tushare_token = os.getenv("TUSHARE_TOKEN")
        _failover = create_default_failover(
            tushare_token=tushare_token,
            use_mock=use_mock,
            enable_baostock=True,
        )
    return _failover


# === 工具实现（直接 def，server.py 中挂装饰器）===

def get_stock_daily(symbol: str, start: str, end: str) -> list:
    """获取 A 股日线数据（多源故障转移）"""
    cache = get_cache()
    key = f"daily:{symbol}:{start}:{end}"
    cached = cache.get(key, ttl=TTL_DAILY)
    if cached is not None:
        return cached
    df = _get_failover().get_daily(symbol, start, end)
    data = df.to_dict(orient="records") if hasattr(df, "to_dict") else df
    cache.set(key, data, ttl=TTL_DAILY)
    return data


def get_stock_realtime(symbol: str) -> dict:
    """获取 A 股实时行情（多源故障转移）"""
    cache = get_cache()
    key = f"realtime:{symbol}"
    cached = cache.get(key, ttl=TTL_REALTIME)
    if cached is not None:
        return cached
    data = _get_failover().get_realtime(symbol)
    cache.set(key, data, ttl=TTL_REALTIME)
    return data


def get_xueqiu_quote(symbol: str) -> dict:
    """通过雪球获取实时行情（需要 token）"""
    import os
    token = os.getenv("XUEQIU_TOKEN")
    if not token:
        return {"error": "XUEQIU_TOKEN not configured", "symbol": symbol}
    # mock 实现（实际生产需调用 xueqiu API）
    return {
        "symbol": symbol,
        "source": "xueqiu",
        "note": "需 XUEQIU_TOKEN 配置",
    }


def push_to_feishu(message: str) -> dict:
    """推送消息到飞书（需要 webhook）"""
    import os
    import requests
    webhook = os.getenv("FEISHU_WEBHOOK")
    if not webhook:
        return {"error": "FEISHU_WEBHOOK not configured", "message": message}
    try:
        r = requests.post(webhook, json={"msg_type": "text", "content": {"text": message}}, timeout=10)
        return {"status": "ok", "response_code": r.status_code}
    except Exception as e:
        return {"error": str(e), "message": message}


# === 注册接口（tradex register(mcp) 风格）===

def register(mcp):
    """注册到 mcp 实例"""
    mcp.tool()(get_stock_daily)
    mcp.tool()(get_stock_realtime)
    mcp.tool()(get_xueqiu_quote)
    mcp.tool()(push_to_feishu)
    return ["get_stock_daily", "get_stock_realtime", "get_xueqiu_quote", "push_to_feishu"]
