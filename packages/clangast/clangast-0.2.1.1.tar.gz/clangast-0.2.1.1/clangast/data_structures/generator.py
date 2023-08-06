from typing import Any, NoReturn, Deque, Sized, Iterator, Union, Iterable

from collections import deque


class EndlessPipeline(object):
    def __init__(self, source: Iterable[Any]):
        self.pipeline = source

    def __next__(self) -> Any:
        for element in self.pipeline:
            return element

    def __iter__(self) -> Any:
        t = next(self)
        while t is not None:
            yield t
            t = next(self)

    def pop(self) -> Any:
        return next(self)


class DefaultStack(object):
    def __init__(self):
        self.collection: Deque[Any] = deque()

    def __len__(self) -> int:
        return len(self.collection)

    def __next__(self) -> Any:
        while len(self) != 0:
            return self.collection.pop()

    def __add__(self, other: Any) -> NoReturn:
        self.collection.append(other)


class StackingPipeline(EndlessPipeline):
    def __init__(self, source: Iterable[Any], stacking_container: Iterator[Any] = None):
        super(StackingPipeline, self).__init__(source)
        if stacking_container is None:
            stacking_container = DefaultStack()
        self.stack = stacking_container

    def __next__(self) -> Any:
        while len(self.stack) != 0:
            return next(self.stack)
        return super(StackingPipeline, self).__next__()

    def __iter__(self) -> Any:
        t = next(self)
        while t is not None:
            yield t
            t = next(self)

    def __add__(self, other: Any) -> NoReturn:
        self.stack += other

    def pop(self) -> Any:
        return next(self)
