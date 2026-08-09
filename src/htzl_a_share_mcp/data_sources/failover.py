"""多源故障转移"""
import pandas as pd
from typing import List
from .base import BaseDataSource


class DataSourceFailover:
    """多源故障转移（Issue #1857 范本扩展）"""

    def __init__(self, sources: List[BaseDataSource]):
        self.sources = sources
        self.cache = {}
        self.last_used_source = None

    def get_daily(self, symbol: str, start: str, end: str, use_cache: bool = True) -> pd.DataFrame:
        cache_key = f"{symbol}_{start}_{end}"
        if use_cache and cache_key in self.cache:
            return self.cache[cache_key]

        for source in self.sources:
            try:
                if not source.is_available():
                    continue
                df = source.get_daily(symbol, start, end)
                if df is not None and not df.empty:
                    self.cache[cache_key] = df
                    self.last_used_source = source.__class__.__name__
                    return df
            except Exception as e:
                print(f"{source.__class__.__name__} 失败：{e}", flush=True)
                continue

        raise RuntimeError(f"所有数据源均失败: {symbol}")

    def get_realtime(self, symbol: str) -> dict:
        for source in self.sources:
            try:
                if not source.is_available():
                    continue
                data = source.get_realtime(symbol)
                if data:
                    self.last_used_source = source.__class__.__name__
                    return data
            except Exception as e:
                print(f"{source.__class__.__name__} 实时行情失败：{e}", flush=True)
                continue
        raise RuntimeError(f"所有数据源均失败: {symbol}")