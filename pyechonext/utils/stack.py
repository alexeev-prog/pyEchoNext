from typing import Any, List


class LIFOStack:
    """
    This class describes a LIFO-stack.
    """

    def __init__(self):
        """
        Constructs a new instance.
        """
        self._items: List[Any] = []

    @property
    def items(self) -> map:
        """
        Get items (reversed)

        :returns:	mapped items
        :rtype:		map
        """
        return reversed(self._items)

    def is_empty(self) -> bool:
        """
        Determines if empty.

        :returns:	True if empty, False otherwise.
        :rtype:		bool
        """
        return len(self._items) == 0

    def push(self, *args):
        """
        Push to stack

        :param		args:  The arguments
        :type		args:  list
        """
        for arg in args:
            self._items.append(arg)

    def pop(self) -> Any:
        """
        Pops the object.

        :returns:	popped object
        :rtype:		Any

        :raises		IndexError:	 stack is empty
        """
        if self.is_empty():
            raise IndexError("LIFO Stack is empty")

        return self._items.pop()

    def peek(self) -> Any:
        """
        Peek the last item

        :returns:	last item
        :rtype:		Any

        :raises		IndexError:	 stack is empty
        """
        if self.is_empty():
            raise IndexError("LIFO Stack is empty")

        return self._items[-1]

    @property
    def size(self) -> int:
        """
        Get items list length

        :returns:	list length
        :rtype:		int
        """
        return len(self._items)

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        :returns:	String representation of the object.
        :rtype:		str
        """
        return " -> ".join(map(str, reversed(self._items)))
