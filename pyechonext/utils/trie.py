from typing import List, Optional


class TrieNode:
    def __init__(self, text: str = "") -> None:
        self.text = text
        self.children = dict()
        self.is_word = False


class PrefixTree:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        current = self.root
        for i, char in enumerate(word):
            if char not in current.children:
                prefix = word[0: i + 1]
                current.children[char] = TrieNode(prefix)
            current = current.children[char]
        current.is_word = True

    def find(self, word: str) -> Optional[str]:
        current = self.root

        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]

        if current.is_word:
            return current

        return None

    def _child_words_for(self, node: TrieNode, words: list) -> None:
        if node.is_word:
            words.append(node.text)

        for letter in node.children:
            self._child_words_for(node.children[letter], words)

    def starts_with(self, prefix: str) -> List[str]:
        words = list()
        current = self.root

        for char in prefix:
            if char not in current.children:
                return list()
            current = current.children[char]

        self._child_words_for(current, words)

        return words

    def size(self, current: Optional[TrieNode] = None) -> int:
        if not current:
            current = self.root

        count = 1

        for letter in current.children:
            count += self.size(current.children[letter])

        return count
