from collections import UserDict, deque


class LimitedDict[Key, Value](UserDict[Key, Value]):
    def __init__(self, *, maxlimit: int = 1000) -> None:
        super().__init__()
        self.maxlimit = maxlimit
        self.queue: deque[Key] = deque(maxlen=maxlimit)

    def set(self, key: Key, value: Value, /) -> Value | None:
        """Set item in the dictionary.
        Returns a value that was deleted when the limit in the dictionary
        was reached, otherwise None.
        """
        deleted_item = None
        if len(self.queue) >= self.maxlimit:
            deleted_item = self.pop(self.queue.popleft(), None)
        if key not in self.queue:
            self.queue.append(key)
        super().__setitem__(key, value)
        return deleted_item

    def __setitem__(self, key: Key, value: Value, /) -> None:
        self.set(key, value)

    def __delitem__(self, key: Key) -> None:
        if key in self.queue:
            self.queue.remove(key)
        return super().__delitem__(key)


__all__ = ("LimitedDict",)
