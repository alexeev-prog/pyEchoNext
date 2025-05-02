import time
from functools import wraps
from typing import Any, Callable, Type

from pyechonext.utils.patterns import Singleton


class PerformanceCacheBase(object):
    """
    An abstract base class for implementing a PerformanceCache.

    This class defines the basic interface for a PerformanceCache, including methods for
    getting, setting, and clearing PerformanceCache entries.
    """

    def get(self, key: str) -> Any:
        """
        Retrieve a value from the PerformanceCache.

        Args: key (str): The key to retrieve.

        Returns: Any: The PerformanceCached value, or None if the key is not found.

        :param		key:  The key
        :type		key:  str

        :returns:	value from PerformanceCache
        :rtype:		Any
        """
        raise NotImplementedError

    def set(self, key: str, value: Any, timestamp: float) -> None:
        """
        Store a value in the PerformanceCache.

        Args: key (str): The key to store the value under. value (Any): The
        value to store. timestamp (float): The timestamp when the value was
        generated.

        :param		key:		The new value
        :type		key:		str
        :param		value:		The value
        :type		value:		Any
        :param		timestamp:	The timestamp
        :type		timestamp:	float

        :returns:	{ description_of_the_return_value }
        :rtype:		None
        """
        raise NotImplementedError

    def clear(self) -> None:
        """
        Clear all entries from the PerformanceCache.
        """
        raise NotImplementedError


class InMemoryPerformanceCache(PerformanceCacheBase):
    """
    An in-memory PerformanceCache implementation.

    This class stores PerformanceCached values in a dictionary, with a separate dictionary
    to track the access times of each entry. Entries are evicted from the PerformanceCache
    when the maximum size is reached or when the time-to-live (TTL) has expired.
    """

    def __init__(self, max_size: int = 1000, ttl: int = 60) -> None:
        """
        Constructs a new instance.

        :param		max_size:  The maximum size
        :type		max_size:  int
        :param		ttl:	   The ttl
        :type		ttl:	   int
        """
        self.max_size = max_size
        self.ttl = ttl
        self.performance_cache = {}
        self.timestamps = {}

    def get(self, key: str) -> Any:
        """
        Gets the specified key.

        :param		key:  The key
        :type		key:  str

        :returns:	Any value
        :rtype:		Any
        """
        if key in self.performance_cache:
            if time.time() - self.timestamps[key] <= self.ttl:
                return self.performance_cache[key]
            else:
                del self.performance_cache[key]
                del self.timestamps[key]
        return None

    def set(self, key: str, value: Any, timestamp: float) -> None:
        """
        Set new PerformanceCache element

        :param		key:		The new value
        :type		key:		str
        :param		value:		The value
        :type		value:		Any
        :param		timestamp:	The timestamp
        :type		timestamp:	float
        """
        if len(self.performance_cache) >= self.max_size:
            oldest_key = min(self.timestamps, key=self.timestamps.get)
            del self.performance_cache[oldest_key]
            del self.timestamps[oldest_key]
        self.performance_cache[key] = value
        self.timestamps[key] = timestamp

    def clear(self) -> None:
        """
        Clears the PerformanceCache
        """
        self.performance_cache.clear()
        self.timestamps.clear()


class PerformanceCacheFactory(object):
    """
    A factory for creating different types of PerformanceCaches.

    This class follows the Factory pattern to provide a consistent interface for
    creating PerformanceCache instances, without exposing the specific implementation details.
    """

    @staticmethod
    def create_performance_cache(
        performance_cache_type: Type[PerformanceCacheBase], *args, **kwargs
    ) -> PerformanceCacheBase:
        """
        Create a new PerformanceCache instance of the specified type.

        Args: performance_cache_type (Type[PerformanceCacheBase]): The type of PerformanceCache to create. *args:
        Positional arguments to pass to the PerformanceCache constructor. **kwargs: Keyword
        arguments to pass to the PerformanceCache constructor.

        Returns: PerformanceCacheBase: A new instance of the specified PerformanceCache type.

        :param		performance_cache_type:	 The PerformanceCache type
        :type		performance_cache_type:	 Type[PerformanceCacheBase]
        :param		args:		 The arguments
        :type		args:		 list
        :param		kwargs:		 The keywords arguments
        :type		kwargs:		 dictionary

        :returns:	The PerformanceCache base.
        :rtype:		PerformanceCacheBase
        """
        return performance_cache_type(*args, **kwargs)


class SingletonPerformanceCache(PerformanceCacheBase, metaclass=Singleton):
    """

    A Singleton PerformanceCache that delegates to a specific PerformanceCache implementation.

    This class follows the Singleton pattern to ensure that there is only one
    instance of the PerformanceCache in the application. It also uses the Factory pattern
    to create the underlying PerformanceCache implementation.
    """

    def __init__(
        self, performance_cache_type: Type[PerformanceCacheBase], *args, **kwargs
    ) -> None:
        """
        Constructs a new instance.

        :param		performance_cache_type:	 The PerformanceCache type
        :type		performance_cache_type:	 Type[PerformanceCacheBase]
        :param		args:		 The arguments
        :type		args:		 list
        :param		kwargs:		 The keywords arguments
        :type		kwargs:		 dictionary
        """
        self.performance_cache = PerformanceCacheFactory.create_performance_cache(
            performance_cache_type, *args, **kwargs
        )

    def get(self, key: str) -> Any:
        """
        Gets the specified key.

        :param		key:  The key
        :type		key:  str

        :returns:	Any value
        :rtype:		Any
        """
        return self.performance_cache.get(key)

    def set(self, key: str, value: Any, timestamp: float) -> None:
        """
        Set new PerformanceCache element

        :param		key:		The new value
        :type		key:		str
        :param		value:		The value
        :type		value:		Any
        :param		timestamp:	The timestamp
        :type		timestamp:	float
        """
        self.performance_cache.set(key, value, timestamp)

    def clear(self) -> None:
        """
        Clear PerformanceCache
        """
        self.performance_cache.clear()


def performance_cached(
    performance_cache: SingletonPerformanceCache,
    key_func: Callable[[Any, Any], str] = lambda *args, **kwargs: str(args)
    + str(kwargs),
) -> Callable:
    """
    A decorator that PerformanceCaches the results of a function or method.

    This decorator uses the provided PerformanceCache instance to store and retrieve the
    results of the decorated function or method. The key_func argument allows
    you to customize how the PerformanceCache key is generated from the function/method
    arguments.

    Args: PerformanceCache (SingletonPerformanceCache): The PerformanceCache instance to use for caching.
    key_func (Callable[[Any, Any], str]): A function that generates the PerformanceCache
    key from the function/method arguments.

    Returns: Callable: A new function or method that PerformanceCaches the results.

    :param		performance_cache:	   The PerformanceCache
    :type		performance_cache:	   SingletonPerformanceCache
    :param		key_func:  The key function
    :type		key_func:  (Callable[[Any, Any], str])

    :returns:	decorator
    :rtype:		Callable
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = key_func(*args, **kwargs)
            cached_value = performance_cache.get(key)
            if cached_value is not None:
                return cached_value
            else:
                result = func(*args, **kwargs)
                performance_cache.set(key, result, time.time())
                return result

        return wrapper

    return decorator
