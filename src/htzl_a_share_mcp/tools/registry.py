"""
tools/registry.py — 工具注册中心（参考 wolfjkd/tradex-hub tools/registry.py）

设计原则：
1. 自动发现：扫描 tools/ 目录下所有 register(mcp) 模块
2. 元数据：每个工具有 name / category / description
3. 双轨制：装饰器注册 + register(mcp) 函数共存

Usage:
    from .registry import register_tool, ToolRegistry
    
    @register_tool("L1-数据获取", "搜索A股股票")
    async def search_stock(keyword: str) -> str: ...
    
    # 或：
    def register(mcp):
        @mcp.tool()
        async def search_stock(keyword: str) -> str: ...
    
    ToolRegistry.auto_discover(importlib.import_module("htzl_a_share_mcp.tools"))
"""

from __future__ import annotations

import importlib
import logging
import pkgutil
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


@dataclass
class ToolMeta:
    """工具元数据。"""
    name: str
    category: str
    description: str
    handler: Callable


# 装饰器 + 注册表（module-level）
_TOOL_REGISTRY: dict[str, ToolMeta] = {}


def _get_registry() -> dict[str, ToolMeta]:
    """获取 module-level 注册表（兼容 class 属性访问）"""
    return _TOOL_REGISTRY


def register_tool(category: str, description: str):
    """装饰器：注册工具元数据"""
    def decorator(func: Callable) -> Callable:
        meta = ToolMeta(
            name=func.__name__,
            category=category,
            description=description,
            handler=func,
        )
        _get_registry()[func.__name__] = meta
        return func
    return decorator


class ToolRegistry:
    """工具注册表 + 自动发现"""

    @classmethod
    def get_all(cls) -> dict[str, ToolMeta]:
        return dict(_get_registry())

    @classmethod
    def get_by_category(cls, category: str) -> list[ToolMeta]:
        return [m for m in _get_registry().values() if m.category == category]

    @classmethod
    def auto_discover(cls, tools_package: Any) -> int:
        """自动发现 tools/ 包下所有模块，收集元数据 + 调用 register(mcp)

        Returns:
            注册的工具数量
        """
        registered = 0
        for mod_info in pkgutil.iter_modules(tools_package.__path__):
            if mod_info.name in ("registry", "__init__"):
                continue
            mod_name = f"{tools_package.__name__}.{mod_info.name}"
            try:
                importlib.import_module(mod_name)
                registered += 1
                logger.debug(f"已加载工具模块: {mod_name}")
            except Exception as e:
                logger.warning(f"模块 {mod_name} 加载失败: {e}")
        return registered

    @classmethod
    def register_all(cls, mcp: Any) -> list[str]:
        """把 _TOOL_REGISTRY 里的工具全部注册到 mcp 实例

        Args:
            mcp: FastMCP 实例

        Returns:
            注册的工具名列表
        """
        names = []
        for meta in _get_registry().values():
            # 装饰器注册的 handler 是原函数，直接用 @mcp.tool()
            # 这里为了避免重复装饰，我们直接调用 handler
            try:
                mcp.tool()(meta.handler)
                names.append(meta.name)
            except Exception as e:
                logger.warning(f"工具 {meta.name} 注册失败: {e}")
        return names

    @classmethod
    def stats(cls) -> dict:
        """返回注册表统计"""
        categories: dict[str, int] = {}
        for meta in _get_registry().values():
            categories[meta.category] = categories.get(meta.category, 0) + 1
        return {
            "total": len(_TOOL_REGISTRY),
            "by_category": categories,
        }


# 兼容 tradex 风格
def register(mcp: Any) -> list[str]:
    """注册到 mcp 实例（tradex 风格接口）"""
    return ToolRegistry.register_all(mcp)
