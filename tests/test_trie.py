# tests/test_trie.py
import pytest
from pyechonext.utils.trie import PrefixTree

class TestPrefixTree:
    @pytest.fixture
    def trie(self):
        trie = PrefixTree()
        words = ["apple", "app", "aposematic", "appreciate", "book", "bad", "bear", "bat"]
        for word in words:
            trie.insert(word)
        return trie

    def test_insert_find(self, trie):
        assert trie.find("app") is not None
        assert trie.find("apple") is not None
        assert trie.find("application") is None

    def test_starts_with(self, trie):
        assert set(trie.starts_with("app")) == {"app", "apple", "appreciate"}
        assert set(trie.starts_with("b")) == {"book", "bad", "bear", "bat"}
        assert set(trie.starts_with("ba")) == {"bad", "bat"}

    def test_size(self, trie):
        assert trie.size() > 0
        assert trie.size(trie.root.children['a']) == 20

    def test_empty_prefix(self, trie):
        assert len(trie.starts_with("")) == 8
