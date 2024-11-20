import time
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


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
		"""
		Constructs a new instance.

		:param		timeout:  The timeout
		:type		timeout:  int
		"""
		self._cache: Dict[str, CacheEntry] = {}
		self._timeout = timeout

	def set(self, key: str, value: Any, **kwargs):
		"""
		Set new item in cache

		:param		key:	 The new value
		:type		key:	 str
		:param		value:	 The value
		:type		value:	 Any
		:param		kwargs:	 The keywords arguments
		:type		kwargs:	 dictionary
		"""
		expiry_time = time.time() + self._timeout

		self._cache[key] = CacheEntry(
			name=key, value=value, expiry=expiry_time, extra_params=kwargs
		)

	def get(self, key: str) -> Optional[Any]:
		"""
		Gets the specified key.

		:param		key:  The key
		:type		key:  str

		:returns:	entry
		:rtype:		Optional[Any]
		"""
		entry = self._cache.get(key)

		if entry is not None and time.time() <= entry.expiry:
			return entry.value
		elif entry is not None and time.time() > entry.expiry:
			self.invalidate(key)

		return None

	def invalidate(self, key: str):
		"""
		Delete item by key from cache

		:param		str:  The key string
		:type		str:  str
		"""
		if key in self._cache:
			del self._cache[key]

	def clean_up(self):
		"""
		Clean up expired items
		"""
		current_time = time.time()
		keys_to_delete = [
			key for key, entry in self._cache.items() if entry.expire < current_time
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
		"""
		Constructs a new instance.

		:param		cache:	The cache
		:type		cache:	InMemoryCache
		"""
		self.cache = cache

	def save(self, key: str, data: Any):
		"""
		Save item

		:param		key:   The key
		:type		key:   str
		:param		data:  The data
		:type		data:  Any
		"""
		self.cache.set(key, data)

	def update(self, key: str, new_data: Any):
		"""
		Update item

		:param		key:	   The key
		:type		key:	   str
		:param		new_data:  The new data
		:type		new_data:  Any
		"""
		self.clear_data(key)
		self.save(key, new_data)

	def clear_data(self, key: str):
		"""
		Clear data

		:param		key:  The key
		:type		key:  str
		"""
		self.cache.invalidate(key)
