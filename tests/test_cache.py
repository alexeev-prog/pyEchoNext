# tests/test_cache.py
import time

import pytest

from pyechonext.cache import Cacheable, CacheEntry, InMemoryCache


class TestCacheEntry:
    def test_entry_creation(self):
        entry = CacheEntry(name="test", value=42, expiry=1000.0)
        assert entry.name == "test"
        assert entry.value == 42
        assert entry.expiry == 1000.0


class TestInMemoryCache:
    @pytest.fixture
    def cache(self):
        return InMemoryCache(timeout=0.1)

    def test_set_and_get(self, cache):
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_expiry(self, cache):
        cache.set("key1", "value1")
        time.sleep(0.2)
        assert cache.get("key1") is None

    def test_invalidate(self, cache):
        cache.set("key1", "value1")
        cache.invalidate("key1")
        assert cache.get("key1") is None

    def test_clean_up(self, cache):
        cache.set("key1", "value1")
        time.sleep(0.2)
        cache.clean_up()
        assert "key1" not in cache._cache

    def test_clear(self, cache):
        cache.set("key1", "value1")
        cache.clear()
        assert not cache._cache


class TestCacheable:
    @pytest.fixture
    def cacheable(self):
        cache = InMemoryCache()
        return Cacheable(cache)

    def test_cache_operations(self, cacheable):
        cacheable.save("key1", "value1")
        assert cacheable.cache.get("key1") == "value1"

        cacheable.update("key1", "value2")
        assert cacheable.cache.get("key1") == "value2"

        cacheable.clear_data("key1")
        assert cacheable.cache.get("key1") is None
