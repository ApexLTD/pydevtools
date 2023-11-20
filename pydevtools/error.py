from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ExistsError(Exception):
    id: Any

    duplicate: Field


@dataclass
class Field:
    name: str
    value: Any

    def __str__(self) -> str:
        return f"{self.name}<{self.value}>"


@dataclass
class DoesNotExistError(Exception):
    id: Any
