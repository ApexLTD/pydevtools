from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self


@dataclass
class _Duplicates:
    fields: list[_Duplicate] = field(default_factory=list)

    def __setitem__(self, key: str, value: Any) -> None:
        self.fields.append(_Duplicate(key, value))

    def __str__(self) -> str:
        return ",".join([str(f) for f in self.fields])

    def __bool__(self) -> bool:
        return bool(self.fields)


@dataclass
class _Duplicate:
    name: str
    value: Any

    def __str__(self) -> str:
        return f"{self.name}<{self.value}>"


@dataclass
class ExistsError(Exception):
    id: Any

    duplicates: _Duplicates = field(default_factory=_Duplicates)

    def and_duplicate(self, **fields: Any) -> Self:
        return self.with_duplicate(**fields)

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
