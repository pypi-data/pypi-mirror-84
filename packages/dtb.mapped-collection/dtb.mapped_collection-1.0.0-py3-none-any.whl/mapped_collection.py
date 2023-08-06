from abc import ABC, abstractmethod
from typing import Collection, Dict, Generic, List, Protocol, TypeVar


class WithKey(Protocol):
    def key(self) -> str:
        ...


T = TypeVar("T", bound=WithKey)


class AbstractMappedCollection(ABC, Generic[T]):
    def __init__(self, items: Collection[T]) -> None:
        self._collection: Dict[str, T] = {}
        for item in items:
            self._collection[item.key()] = item

    def add(self, item: T) -> None:
        self._collection[item.key()] = item

    def as_list(self) -> List[T]:
        return list(self._collection.values())

    def __contains__(self, item: T) -> bool:
        return item.key() in self._collection

    def __getitem__(self, item: str) -> T:
        return self._collection[item]

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass
