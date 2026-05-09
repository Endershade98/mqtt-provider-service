# src/domain/command/value_objects.py

from enum import Enum
from dataclasses import dataclass
from src.domain.shared.value_objects import ValueObject
from src.domain.shared.exceptions import InvalidCommandId


class CommandStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    ACKED = "ACKED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    EXPIRED = "EXPIRED"

@dataclass(frozen=True)
class CommandId(ValueObject):
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or not self.value.strip():
            raise InvalidCommandId("CommandId cannot be empty")
