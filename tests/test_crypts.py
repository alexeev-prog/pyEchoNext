# tests/test_crypts.py
import pytest
from pyechonext.security.crypts import PSPCAlgorithm

class TestPSPCAlgorithm:
    @pytest.fixture
    def algo(self):
        return PSPCAlgorithm(seed=42)

    def test_crypt_decrypt(self, algo):
        original = "secret_password"
        encrypted = algo.crypt(original)
        decrypted = algo.decrypt(encrypted)
        assert decrypted == original

    def test_different_seeds(self):
        algo1 = PSPCAlgorithm(seed=100)
        algo2 = PSPCAlgorithm(seed=200)
        encrypted1 = algo1.crypt("test")
        encrypted2 = algo2.crypt("test")
        assert encrypted1 != encrypted2

    def test_empty_string(self, algo):
        assert algo.crypt("") == ""
        assert algo.decrypt("") == ""
