"""
utils/cache.py — 两级 TTL 缓存（参考 wolfjkd/tradex-hub utils/cache.py）

Caching strategy:
- 实时行情 (realtime):   30 秒  (memory only)
- 日线数据 (daily):       300 秒 (memory + file)
- 财务报表 (financial):   86400 秒 (memory + file)
- 公司信息 (company):     86400 秒 (memory + file)
- 宏观数据 (macro):       604800 秒 (memory + file)

Two-level cache:
- Level 1: In-memory LRU with TTL (fast, volatile)
- Level 2: File-based JSON cache (persistent across restarts, ~/.htzl_a_share_cache/)

Thread-safe with threading.Lock.
"""

import hashlib
import json
import logging
import os
import time
import threading
from pathlib import Path
from typing import Any, Optional
from collections import OrderedDict

logger = logging.getLogger(__name__)

# TTL 预设（秒）
TTL_REALTIME = 30         # 实时行情
TTL_DAILY = 300           # 日线 5 分钟
TTL_FINANCIAL = 86400     # 财报 24 小时
TTL_COMPANY = 86400       # 公司信息 24 小时
TTL_MACRO = 604800        # 宏观数据 7 天

# 文件缓存阈值（超过此值同时写文件）
FILE_CACHE_TTL_THRESHOLD = 3600  # 1 小时


def _default_cache_dir() -> Path:
    """默认缓存目录 ~/.htzl_a_share_cache/"""
    env_dir = os.getenv("HTZL_CACHE_DIR")
    if env_dir:
        return Path(env_dir)
    return Path.home() / ".htzl_a_share_cache"


class TTLCache:
    """线程安全 TTL 缓存，基于 OrderedDict + LRU 淘汰。

    Args:
        max_size: 最大条目数，0 = 无限制（默认 5000）
    """

    def __init__(self, max_size: int = 5000):
        self._store: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self._max_size = max_size
        self._lock = threading.Lock()
        self._hit_count: int = 0
        self._miss_count: int = 0

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值，过期返回 None。"""
        with self._lock:
            if key in self._store:
                value, expires_at = self._store[key]
                if time.time() < expires_at:
                    self._store.move_to_end(key)  # LRU
                    self._hit_count += 1
                    return value
                del self._store[key]
            self._miss_count += 1
        return None

    def set(self, key: str, value: Any, ttl: int = TTL_DAILY) -> None:
        """设置缓存值，ttl 秒后过期。"""
        with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = (value, time.time() + ttl)
            while self._max_size > 0 and len(self._store) > self._max_size:
                self._store.popitem(last=False)

    def delete(self, key: str) -> None:
        """删除指定 key。"""
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        """清空所有缓存。"""
        with self._lock:
            self._store.clear()
            self._hit_count = 0
            self._miss_count = 0

    def stats(self) -> dict:
        """返回缓存统计信息。"""
        with self._lock:
            total = self._hit_count + self._miss_count
            hit_rate = self._hit_count / total if total > 0 else 0.0
            return {
                "size": len(self._store),
                "max_size": self._max_size,
                "hits": self._hit_count,
                "misses": self._miss_count,
                "hit_rate": f"{hit_rate:.2%}",
            }


class TwoLevelCache:
    """两级缓存：memory LRU + file JSON。

    Args:
        cache_dir: 文件缓存目录，默认 ~/.htzl_a_share_cache/
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        self._memory = TTLCache(max_size=5000)
        self._cache_dir = cache_dir or _default_cache_dir()
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _file_path(self, key: str) -> Path:
        """根据 key 生成文件路径（用 SHA256 避免特殊字符）。"""
        h = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
        return self._cache_dir / f"{h}.json"

    def get(self, key: str, ttl: int = TTL_DAILY) -> Optional[Any]:
        """先查内存，再查文件。"""
        # Level 1: memory
        value = self._memory.get(key)
        if value is not None:
            return value

        # Level 2: file
        if ttl < FILE_CACHE_TTL_THRESHOLD:
            # 短 TTL 不写文件
            return None

        path = self._file_path(key)
        if not path.exists():
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if time.time() < payload.get("expires_at", 0):
                # 提升到 memory
                self._memory.set(key, payload["value"], ttl=ttl)
                return payload["value"]
            path.unlink(missing_ok=True)
        except (json.JSONDecodeError, KeyError, OSError) as e:
            logger.warning(f"Cache read error for {key}: {e}")

        return None

    def set(self, key: str, value: Any, ttl: int = TTL_DAILY) -> None:
        """写入 memory + file（如果 TTL 足够长）。"""
        # Level 1: memory
        self._memory.set(key, value, ttl=ttl)

        # Level 2: file（仅长期缓存）
        if ttl < FILE_CACHE_TTL_THRESHOLD:
            return

        path = self._file_path(key)
        payload = {
            "value": value,
            "expires_at": time.time() + ttl,
            "key": key,
            "ttl": ttl,
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, default=str)
        except OSError as e:
            logger.warning(f"Cache write error for {key}: {e}")

    def clear(self) -> None:
        """清空 memory + file。"""
        self._memory.clear()
        for path in self._cache_dir.glob("*.json"):
            path.unlink(missing_ok=True)

    def stats(self) -> dict:
        """返回缓存统计。"""
        file_count = len(list(self._cache_dir.glob("*.json")))
        mem_stats = self._memory.stats()
        mem_stats["file_count"] = file_count
        mem_stats["cache_dir"] = str(self._cache_dir)
        return mem_stats


# 全局单例
_default_cache: Optional[TwoLevelCache] = None


def get_cache() -> TwoLevelCache:
    """获取全局缓存单例。"""
    global _default_cache
    if _default_cache is None:
        _default_cache = TwoLevelCache()
    return _default_cache
