from abc import ABC, abstractmethod
from typing import Collection, Dict, Generic, List, Protocol, TypeVar


class WithKey(Protocol):
    def key(self) -> str:
        ...


T = TypeVar("T", bound=WithKey)


class AbstractMappedCollection(ABC, Generic[T]):
    _collection: Dict[str, T]

    def __init__(self, items: Collection[T]) -> None:
        ...

    def add(self, item: T) -> None:
        ...

    def as_list(self) -> List[T]:
        ...

    def __contains__(self, item: T) -> bool:
        ...

    def __getitem__(self, item: str) -> T:
        ...

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...
