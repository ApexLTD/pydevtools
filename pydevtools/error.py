from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, Self


@dataclass
class ExistsError(Exception):
    id: Any
    item: Any = None

    _duplicates: list[Criteria] = field(init=False, default_factory=list)

    def with_duplicate(self, criteria: Criteria) -> Self:
        self._duplicates.append(criteria)

        return self

    def __str__(self) -> str:
        return ",".join([f"{criteria(self.item)}" for criteria in self._duplicates])

    def fire(self) -> None:
        if self._duplicates:
            raise self


@dataclass
class DoesNotExistError(Exception):
    id: Any


class Criteria(Protocol):
    def __call__(self, item: Any) -> str:
        pass
