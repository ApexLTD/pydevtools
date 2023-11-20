from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self


@dataclass
class ExistsError(Exception):
    id: Any

    duplicates: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return ",".join([f"{k}<{v}>" for k, v in self.duplicates.items()])

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
