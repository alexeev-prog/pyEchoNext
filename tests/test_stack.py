# tests/test_stack.py
import pytest

from pyechonext.utils.stack import LIFOStack


class TestLIFOStack:
    @pytest.fixture
    def stack(self):
        return LIFOStack()

    def test_push_pop(self, stack):
        stack.push(1, 2, 3)
        assert stack.pop() == 3
        assert stack.pop() == 2
        assert stack.pop() == 1

    def test_peek(self, stack):
        stack.push(42)
        assert stack.peek() == 42
        assert stack.size == 1

    def test_empty_stack(self, stack):
        with pytest.raises(IndexError):
            stack.pop()
        with pytest.raises(IndexError):
            stack.peek()

    def test_size(self, stack):
        stack.push(1, 2, 3)
        assert stack.size == 3
        stack.pop()
        assert stack.size == 2

    def test_items_reversed(self, stack):
        stack.push(1, 2, 3)
        assert list(stack.items) == [3, 2, 1]
