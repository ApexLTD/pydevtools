from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self, Protocol


@dataclass
class ExistsError(Exception):
    id: Any
    item: Any = None

    _duplicates: dict[str, Any] = field(init=False, default_factory=dict)

    def with_duplicate(self, criteria: Criteria) -> Self:
        self._duplicates[criteria.name] = criteria(self.item)

        return self

    def __str__(self) -> str:
        return ",".join([f"{k}<{v}>" for k, v in self._duplicates.items()])

    def fire(self) -> None:
        if self._duplicates:
            raise self


@dataclass
class DoesNotExistError(Exception):
    id: Any


class Criteria(Protocol):
    name: str

    def __call__(self, item: Any) -> Any:
        pass
