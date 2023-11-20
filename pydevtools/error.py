from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self


@dataclass
class _Duplicates(dict[str, Any]):
    def __str__(self) -> str:
        return ",".join([f"{k}<{v}>" for k, v in self.items()])


@dataclass
class ExistsError(Exception):
    id: Any

    duplicates: _Duplicates = field(default_factory=_Duplicates)

    def __str__(self) -> str:
        return str(self.duplicates)

    def with_duplicate(self, **fields: Any) -> Self:
        for key, value in fields.items():
            self.duplicates[key] = value

        return self

    def fire(self) -> None:
        if self.duplicates:
            raise self


@dataclass
class DoesNotExistError(Exception):
    id: Any
