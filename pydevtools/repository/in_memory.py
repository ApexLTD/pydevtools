from dataclasses import dataclass, field
from typing import Any, Generic, Iterator, Protocol, Self, TypeVar

from pydevtools.error import Criteria, DoesNotExistError, ExistsError


class _Item(Protocol):
    id: Any


ItemT = TypeVar("ItemT", bound=_Item)


@dataclass
class Attribute:
    name: str

    def __call__(self, item: Any) -> Any:
        return f"{self.name}<{getattr(item, self.name)}>"


@dataclass
class InMemoryRepository(Generic[ItemT]):
    items: dict[str, ItemT] = field(default_factory=dict)

    _uniques: list[Criteria] = field(init=False, default_factory=list)
    _search_by: list[str] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self._search_by = ["id", *self._search_by]

    def with_searchable(self, attribute: str) -> Self:
        self._search_by.append(attribute)

        return self

    def with_unique(self, name: Criteria) -> Self:
        self._uniques.append(name)

        return self

    def create_many(self, items: list[ItemT]) -> None:
        for item in items:
            self.create(item)

    def create(self, item: ItemT) -> None:
        self._ensure_does_not_exist(item)
        self.items[str(item.id)] = item

    def _ensure_does_not_exist(self, item: ItemT) -> None:
        for existing in self.items.values():
            error = ExistsError(existing.id, item=existing)

            for criteria in self._uniques:
                if criteria(item) == criteria(existing):
                    error.with_duplicate(criteria)

            error.fire()

        assert str(item.id) not in self.items, f"Item with id<{item.id}> already exists"

    def read(self, item_id: Any) -> ItemT:
        for item in self.items.values():
            for attribute in self._search_by:
                if getattr(item, attribute) == item_id:
                    return item

        raise DoesNotExistError(item_id)

    def update(self, item: ItemT) -> None:
        self.delete(item.id)
        self.create(item)

    def delete(self, item_id: Any) -> None:
        del self.items[str(item_id)]

    def __iter__(self) -> Iterator[ItemT]:
        yield from self.items.values()

    def __len__(self) -> int:
        return len(self.items)
