import typing
from collections import UserDict, deque

KT = typing.TypeVar("KT")
VT = typing.TypeVar("VT")


class LimitedDict(UserDict[KT, VT]):
    def __init__(self, *, maxlimit: int = 1000) -> None:
        super().__init__()
        self.maxlimit = maxlimit
        self.queue: deque[KT] = deque(maxlen=maxlimit)

    def __setitem__(self, key: KT, value: VT, /) -> None:
        if len(self.queue) >= self.maxlimit:
            self.pop(self.queue.popleft(), None)
        if key not in self.queue:
            self.queue.append(key)
        super().__setitem__(key, value)
    
    def __delitem__(self, key: KT) -> None:
        if key in self.queue:
            self.queue.remove(key)
        return super().__delitem__(key)


__all__ = ("LimitedDict",)
