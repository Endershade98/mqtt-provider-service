# src/domain/shared/base.py
from dataclasses import dataclass, field
from typing import Any
import uuid


@dataclass
class Entity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id