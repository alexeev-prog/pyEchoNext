from typing import Any, List


class LIFOStack:
    """
    This class describes a LIFO-stack.
    """

    __slots__ = "_stack_items"

    def __init__(self):
        """
        Constructs a new instance.
        """
        self._stack_items: List[Any] = []

    @property
    def items(self) -> Any:
        """Get reversed stack items

        Returns:
            Any: reversed stack items
        """
        return reversed(self._stack_items)

    def is_empty(self) -> bool:
        """Determines is empty

        Returns:
            bool: true is empty, false otherwise
        """
        return len(self._stack_items) == 0

    def push(self, *args):
        """Push item to stack items"""
        self._stack_items += args

    def pop(self) -> Any:
        """Pop the object

        Raises:
            IndexError: stack if empty

        Returns:
            Any: stack items with popped item
        """
        if self.is_empty():
            raise IndexError("LIFO Stack is empty")

        return self._stack_items.pop()

    def peek(self) -> Any:
        """Peek the last item

        Raises:
            IndexError: stack is empty

        Returns:
            Any: stack item
        """
        if self.is_empty():
            raise IndexError("LIFO Stack is empty")

        return self._stack_items[-1]

    @property
    def size(self) -> int:
        """Get stack length

        Returns:
            int: length of stack items
        """
        return len(self._stack_items)

    def __str__(self) -> str:
        """String representation of object

        Returns:
            str: string representation
        """
        return " -> ".join(map(str, reversed(self._stack_items)))
