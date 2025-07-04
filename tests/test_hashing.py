# tests/test_hashing.py
import pytest

from pyechonext.security.hashing import (HashAlgorithm, PlainHasher,
                                         SaltedHasher)


class TestHashing:
    @pytest.mark.parametrize(
        "algorithm", [HashAlgorithm.SHA256, HashAlgorithm.SHA512, HashAlgorithm.MD5]
    )
    def test_plain_hasher(self, algorithm):
        hasher = PlainHasher(algorithm)
        data = "password123"
        hashed = hasher.hash(data)
        assert hasher.verify(data, hashed) is True
        assert hasher.verify("wrong", hashed) is False

    def test_salted_hasher(self):
        hasher = SaltedHasher(salt="unique_salt")
        data = "secure_data"
        hashed = hasher.hash(data)
        assert hasher.verify(data, hashed) is True

        # Different salt should produce different hash
        diff_salt_hasher = SaltedHasher(salt="different_salt")
        assert diff_salt_hasher.verify(data, hashed) is False

    def test_hash_types(self):
        hasher = PlainHasher()
        assert isinstance(hasher.hash("text"), bytes)
        assert isinstance(hasher.hash(b"bytes"), bytes)
