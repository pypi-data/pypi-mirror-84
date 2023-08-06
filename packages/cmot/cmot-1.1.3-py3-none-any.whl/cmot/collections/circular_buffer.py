"""A Circular Buffer"""
from __future__ import annotations

import itertools
from typing import (
    Any,
    Iterable,
    Iterator,
    List,
    MutableSequence,
    Optional,
    TypeVar,
    Union,
    overload,
)

__all__ = ["CircularBuffer"]

T = TypeVar("T")


class CircularBuffer(MutableSequence[T]):
    """A Circular Buffer

    Stores a bounded number of elements in a list-like structure.
    Pushes to one end will drop an element from the other end if necessary.
    Like deque but with efficient random access.

    Complexity:
        - O(1) indexing (get or set)
        - O(1) append / pop to either end
        - O(n) random insert / delete
    """

    def __init__(self, maxlen: int, data: Optional[Iterable[T]] = None):
        """Initialize a CircularBuffer

        Args:
            maxlen: Maximum number of elements.
            data: Optional initial data.
        """
        self._start = 0
        self._end = 0
        # Data can grow to contain `maxlen + 1` elements
        # This enables distinguishing full vs empty states based on start/end indices.
        # Invariant:
        # If len(self._max_data_len) < self._max_data_len then self._start == 0
        if maxlen < 0:
            raise ValueError("must have maxlen >= 0")
        self._max_data_len = maxlen + 1
        if data:
            data_iter = iter(data)
            self._data: List[Optional[T]] = list(itertools.islice(data_iter, maxlen))
            self._end = len(self._data)
            self.extend(data_iter)
        else:
            self._data = []

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return f"{self.__class__.__name__}({self._max_data_len-1!r}, {list(self)!r})"

    def __len__(self):
        if self._end >= self._start:
            return self._end - self._start
        else:
            # Data maxlen minus number of empty elements between start/end
            return self._max_data_len - (self._start - self._end)

    @property
    def maxlen(self) -> int:
        return self._max_data_len - 1

    def _data_index(self, index: int) -> int:
        if index < 0:
            index += len(self)
        i = self._start + index
        if i >= self._max_data_len:
            i -= self._max_data_len
            if i >= self._end:
                raise IndexError(index)
        elif i < 0:
            raise IndexError(index)
        return i

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> MutableSequence[T]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, MutableSequence[T]]:
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self)))]
        result = self._data[self._data_index(index)]
        assert result is not None
        return result

    @overload
    def __setitem__(self, index: int, value: T) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[T]) -> None:
        ...

    def __setitem__(
        self, index: Union[int, slice], value: Union[T, Iterable[T]]
    ) -> None:
        if isinstance(index, slice):
            assert isinstance(value, Iterable)
            value_iter = iter(value)
            for i in range(*index.indices(len(self))):
                self[i] = next(value_iter)
            return

        assert not isinstance(value, Iterable)
        self._data[self._data_index(index)] = value

    def __delitem__(self, index: Union[int, slice]) -> None:
        if isinstance(index, slice):
            for i in sorted(range(*index.indices(len(self))), reverse=True):
                del self[i]
            return

        i = self._data_index(index)
        start = self._start
        last = (self._end - 1) % self._max_data_len
        if i < start or (start <= last) and (i - start) >= (last - i):
            # Shift end of buffer
            self._data[i:last] = self._data[i + 1 : last + 1]
            self._data[last] = None
            self._end = last
        else:
            # Shift start of buffer
            self._data[start + 1 : i + 1] = self._data[start:i]
            self._data[start] = None
            self._start = (self._start + 1) % self._max_data_len

    def insert(self, index: int, value: T) -> None:
        """Insert a new element, dropping from the start of the buffer if necessary."""
        if index < 0:
            index = len(self) + index
        index = min(max(0, index), self._max_data_len - 2)

        if len(self._data) < self._max_data_len:
            assert self._start == 0
            self._end += 1
            if self._end == self._max_data_len:
                self._end = 0
                self._start += 1
                index += 1
            self._data.insert(index, value)
            return

        slot = self._end
        self._end = (self._end + 1) % self._max_data_len
        if self._end == self._start:
            self._start = (self._start + 1) % self._max_data_len
        i = (index + self._start) % self._max_data_len

        if i <= slot:
            self._data[i + 1 : slot + 1] = self._data[i:slot]
            self._data[i] = value
        else:
            self._data[1 : slot + 1] = self._data[:slot]
            self._data[0] = self._data[-1]
            self._data[i + 1 :] = self._data[i:-1]
            self._data[i] = value

    def appendleft(self, value: T) -> None:
        """Insert a new element at the start, dropping from the end if necessary."""
        if len(self._data) < self._max_data_len:
            # Can only insert quickly if data has full size
            self._data += [None] * (self._max_data_len - len(self._data))
        self._start = (self._start - 1) % self._max_data_len
        if self._end == self._start:
            self._end = (self._end - 1) % self._max_data_len
        self._data[self._start] = value

    def extendleft(self, values: Iterable[T]) -> None:
        for v in values:
            self.appendleft(v)

    def popleft(self) -> T:
        """Remove and return the leftmost element."""
        if self._start == self._end:
            raise IndexError("pop from empty buffer")
        value = self._data[self._start]
        assert value is not None
        self._data[self._start] = None
        self._start = (self._start + 1) % self._max_data_len
        return value

    def __iter__(self) -> Iterator[T]:
        # ignoring Optional[T] -> T type mismatch (should never be None)
        if self._end >= self._start:
            yield from iter(self._data[self._start : self._end])  # type: ignore
        else:
            yield from iter(self._data[self._start :])  # type: ignore
            yield from iter(self._data[: self._end])  # type: ignore

    def __reversed__(self) -> Iterator[T]:
        # ignoring Optional[T] -> T type mismatch (should never be None)
        if self._end >= self._start:
            yield from reversed(self._data[self._start : self._end])  # type: ignore
        else:
            yield from reversed(self._data[: self._end])  # type: ignore
            yield from reversed(self._data[self._start :])  # type: ignore

    def __contains__(self, value: Any) -> bool:
        if self._end >= self._start:
            return value in self._data[self._start : self._end]
        else:
            return (
                value in self._data[self._start :] or value in self._data[: self._end]
            )
