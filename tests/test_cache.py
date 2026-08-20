"""utils/cache.py 单元测试"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from htzl_a_share_mcp.utils.cache import (
    TTLCache, TwoLevelCache, get_cache,
    TTL_REALTIME, TTL_DAILY, TTL_FINANCIAL,
)


class TestTTLCache:
    """TTLCache 内存缓存测试"""

    def test_basic_set_get(self):
        cache = TTLCache()
        cache.set("key1", {"price": 100}, ttl=60)
        assert cache.get("key1") == {"price": 100}
        assert cache.stats()["hits"] == 1

    def test_ttl_expiry(self):
        cache = TTLCache()
        cache.set("key1", "value", ttl=1)
        assert cache.get("key1") == "value"
        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_lru_eviction(self):
        cache = TTLCache(max_size=3)
        cache.set("k1", 1, ttl=60)
        cache.set("k2", 2, ttl=60)
        cache.set("k3", 3, ttl=60)
        cache.set("k4", 4, ttl=60)  # 触发 LRU 淘汰 k1
        assert cache.get("k1") is None
        assert cache.get("k2") == 2
        assert cache.get("k3") == 3
        assert cache.get("k4") == 4

    def test_stats(self):
        cache = TTLCache()
        cache.set("k1", "v", ttl=60)
        cache.get("k1")  # hit
        cache.get("k2")  # miss
        stats = cache.stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert "50.00%" in stats["hit_rate"]  # 1 hit + 1 miss


class TestTwoLevelCache:
    """TwoLevelCache 两级缓存测试"""

    def test_memory_only_short_ttl(self):
        """短 TTL 不写文件"""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            cache = TwoLevelCache(Path(tmp))
            cache.set("realtime_price", {"price": 100}, ttl=TTL_REALTIME)
            assert cache.get("realtime_price") == {"price": 100}
            assert cache.stats()["file_count"] == 0

    def test_long_ttl_writes_to_file(self):
        """长 TTL 写文件"""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            cache = TwoLevelCache(Path(tmp))
            cache.set("financial_report", {"revenue": 1e9}, ttl=TTL_FINANCIAL)
            assert cache.stats()["file_count"] == 1

    def test_file_persistence(self):
        """文件缓存持久化"""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            cache1 = TwoLevelCache(Path(tmp))
            cache1.set("data", {"v": 1}, ttl=TTL_FINANCIAL)
            # 新 cache 实例（模拟重启）
            cache2 = TwoLevelCache(Path(tmp))
            assert cache2.get("data", ttl=TTL_FINANCIAL) == {"v": 1}


class TestGlobalCache:
    """全局缓存单例测试"""

    def test_get_cache_singleton(self):
        c1 = get_cache()
        c2 = get_cache()
        assert c1 is c2


def test_all():
    """运行所有测试"""
    test_classes = [TestTTLCache, TestTwoLevelCache, TestGlobalCache]
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
                    print(f"  ✗ {cls.__name__}.{method}: {e}")
    print(f"\n{passed}/{total} tests passed")
    assert passed == total


if __name__ == "__main__":
    test_all()
