import hashlib
from abc import ABC, abstractmethod
from enum import Enum, auto
from hmac import compare_digest
from typing import Union
from collections import Counter


def distribute(items, num_containers, hash_function=hash):
	"""
	Distribute hash function

	:param		items:			 The items
	:param		num_containers:	 The number containers
	:param		hash_function:	 The hash function
	"""
	return Counter([hash_function(item) % num_containers for item in items])


def plot(histogram):
	"""
	Plot simple historgram

	:param		histogram:	The histogram
	:type		histogram:	dict
	"""
	for key in sorted(histogram):
		count = histogram[key]
		padding = (max(histogram.values()) - count) * " "
		print(f"{key:3} {'■' * count}{padding} ({count})")


def hash_function(key):
	"""
	Hash function

	:param		key:  The key
	:type		key:  str

	:returns:	sum
	:rtype:		sum
	"""
	return sum(
		index * ord(character)
		for index, character in enumerate(repr(key).lstrip("'"), 1)
	)


class HashAlgorithm(Enum):
	"""
	This class describes a hash algorithms.
	"""

	SHA256 = auto()
	SHA512 = auto()
	MD5 = auto()
	BLAKE2B = auto()
	BLAKE2S = auto()


class HashingBase(ABC):
	"""
	This class describes a hashing base.
	"""

	@abstractmethod
	def hash(
		self, data: Union[bytes, str], hexdigest: bool = False
	) -> Union[bytes, str]:
		"""
		Hash

		:param		data:				  The data
		:type		data:				  Union[bytes, str]
		:param		hexdigest:			  The hexdigest
		:type		hexdigest:			  bool

		:returns:	hashing
		:rtype:		Union[bytes, str]

		:raises		NotImplementedError:  abstract method
		"""
		raise NotImplementedError()

	@abstractmethod
	def verify(self, data: Union[bytes, str], hashed_data: Union[bytes, str]) -> bool:
		"""
		Verify data and hashed data

		:param		data:				  The data
		:type		data:				  Union[bytes, str]
		:param		hashed_data:		  The hashed data
		:type		hashed_data:		  Union[bytes, str]

		:returns:	true if data=hashed_data
		:rtype:		bool

		:raises		NotImplementedError:  { exception_description }
		"""
		raise NotImplementedError()


class PlainHasher(HashingBase):
	"""
	This class describes a plain hasher.
	"""

	def __init__(self, algorithm: HashAlgorithm = HashAlgorithm.SHA256):
		"""
		Constructs a new instance.

		:param		algorithm:	The algorithm
		:type		algorithm:	HashAlgorithm
		"""
		self.algorithm = algorithm

	def hash(self, data: Union[bytes, str]) -> bytes:
		"""
		Generate hash

		:param		data:  The data
		:type		data:  Union[bytes, str]

		:returns:	hash
		:rtype:		bytes
		"""
		if isinstance(data, str):
			data = data.encode("utf-8")

		hasher = self._get_hasher()
		return hasher(data).digest()

	def verify(self, data: Union[bytes, str], hashed_data: Union[bytes, str]) -> bool:
		"""
		Verify data and hashed data

		:param		data:		  The data
		:type		data:		  Union[bytes, str]
		:param		hashed_data:  The hashed data
		:type		hashed_data:  Union[bytes, str]

		:returns:	true if data==hashed_data
		:rtype:		bool
		"""
		if isinstance(data, str):
			data = data.encode("utf-8")
		if isinstance(hashed_data, str):
			hashed_data = hashed_data.encode()

		expected_hash = self.hash(data)

		return compare_digest(expected_hash, hashed_data)

	def _get_hasher(self) -> callable:
		"""
		Gets the hasher function.

		:returns:	The hasher.
		:rtype:		callable

		:raises		ValueError:	 unknown hash function.
		"""
		hash_functions = {
			HashAlgorithm.SHA256: hashlib.sha256,
			HashAlgorithm.SHA512: hashlib.sha512,
			HashAlgorithm.MD5: hashlib.md5,
			HashAlgorithm.BLAKE2B: hashlib.blake2b,
			HashAlgorithm.BLAKE2S: hashlib.blake2s,
		}

		hash_function = hash_functions.get(self.algorithm, None)

		if hash_function is None:
			raise ValueError(f"Unknown hash function type: {self.algorithm}")
		else:
			return hash_function


class SaltedHasher(HashingBase):
	"""
	This class describes a salted hasher.
	"""

	def __init__(
		self, algorithm: HashAlgorithm = HashAlgorithm.SHA256, salt: str = "SOMESALT"
	):
		"""
		Constructs a new instance.

		:param		algorithm:	The algorithm
		:type		algorithm:	HashAlgorithm
		:param		salt:		The salt
		:type		salt:		str
		"""
		self.algorithm = algorithm
		self.salt = salt

	def hash(self, data: Union[bytes, str]) -> bytes:
		"""
		Generate hash

		:param		data:  The data
		:type		data:  Union[bytes, str]

		:returns:	hash
		:rtype:		bytes
		"""
		salt = self.salt.encode("utf-8")

		if isinstance(data, str):
			data = data.encode("utf-8")

		hasher = self._get_hasher()
		value = f"{data}{salt}".encode("utf-8")

		return hasher(value).digest()

	def verify(self, data: str, hashed_data: Union[bytes, str]) -> bool:
		"""
		Verify data and hashed_data

		:param		data:		  The data
		:type		data:		  str
		:param		hashed_data:  The hashed data
		:type		hashed_data:  Union[bytes, str]

		:returns:	true if data==hashed_data
		:rtype:		bool
		"""
		if isinstance(hashed_data, str):
			print("convert")

		expected_hash = self.hash(data)

		return compare_digest(expected_hash, hashed_data)

	def _get_hasher(self) -> callable:
		"""
		Gets the hasher function.

		:returns:	The hasher.
		:rtype:		callable

		:raises		ValueError:	 unknown hasher function
		"""
		hash_functions = {
			HashAlgorithm.SHA256: hashlib.sha256,
			HashAlgorithm.SHA512: hashlib.sha512,
			HashAlgorithm.MD5: hashlib.md5,
			HashAlgorithm.BLAKE2B: hashlib.blake2b,
			HashAlgorithm.BLAKE2S: hashlib.blake2s,
		}

		hash_function = hash_functions.get(self.algorithm, None)

		if hash_function is None:
			raise ValueError(f"Unknown hash function type: {self.algorithm}")
		else:
			return hash_function
