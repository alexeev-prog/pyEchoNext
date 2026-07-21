import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class CacheEntry:
    """
    This class describes a cache entry.
    """

    name: str
    value: Any
    expiry: float

    extra_params: dict = field(default_factory=dict)


class InMemoryCache:
    """
    This class describes in memory cache.
    """

    def __init__(self, timeout: int = 300):
        """Initialize InMemoryCace

            Args:
        timeout (int, optional): _description_. Defaults to 300.
        """
        self._cache: Dict[str, CacheEntry] = {}
        self._timeout: int = timeout

    def set(self, key: str, value: Any, **kwargs):
        """Set item into cache

            Args:
        key (str): key
        value (Any): value
        """
        expiry_time = time.time() + self._timeout

        self._cache[key] = CacheEntry(
            name=key, value=value, expiry=expiry_time, extra_params=kwargs
        )

    def get(self, key: str) -> Optional[Any]:
        """Get item by specified key

            Args:
        key (str): key item

            Returns:
        Optional[Any]: item value
        """
        entry = self._cache.get(str(key))

        if entry is not None and time.time() <= entry.expiry:
            return entry.value
        elif entry is not None and time.time() > entry.expiry:
            self.invalidate(key)

        return None

    def invalidate(self, key: str):
        """Invalidate item by key

            Args:
        key (str): item key
        """
        if key in self._cache:
            del self._cache[key]

    def clean_up(self):
        """
        Clean up cache
        """
        current_time = time.time()
        keys_to_delete = [
            key for key, entry in self._cache.items() if entry.expiry < current_time
        ]

        for key in keys_to_delete:
            del self._cache[key]

    def clear(self):
        """
        Clears all items
        """
        self._cache.clear()


class Cacheable:
    """
    This class describes a Interface for caching.
    """

    def __init__(self, cache: InMemoryCache):
        """Initialize Cachable Interace

            Args:
        cache (InMemoryCache): cache instance
        """
        self.cache = cache

    def save(self, key: str, data: Any):
        """Save item in cache

            Args:
        key (str): item key
        data (Any): item data
        """
        self.cache.set(key, data)

    def update(self, key: str, new_data: Any):
        """Update item by key

            Args:
        key (str): item key
        new_data (Any): new item data
        """
        self.clear_data(key)
        self.save(key, new_data)

    def clear_data(self, key: str):
        """Clear item data by key

            Args:
        key (str): item key
        """
        self.cache.invalidate(key)
