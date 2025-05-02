from pyechonext.utils.trie import PrefixTree, TrieNode


def test_trienode():
    tn = TrieNode()
    assert not tn.is_word
    assert tn.text == ""
    assert tn.children == {}


def test_trie():
    trie = PrefixTree()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("aposematic")
    trie.insert("appreciate")
    trie.insert("book")
    trie.insert("bad")
    trie.insert("bear")
    trie.insert("bat")

    assert trie.starts_with("app") == ["app", "apple", "appreciate"]

    router_tree = PrefixTree()
    router_tree.insert("index")
    router_tree.insert("users")
    router_tree.insert("transactions")
    router_tree.insert("wallets")
    router_tree.insert("wallets/create")

    assert router_tree.starts_with("wa") == ["wallets", "wallets/create"]
