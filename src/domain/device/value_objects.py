# src/domain/device/value_objects.py
from dataclasses import dataclass
from src.domain.shared.value_objects import ValueObject


@dataclass(frozen=True)
class DeviceId(ValueObject):
    value: str

@dataclass(frozen=True)
class CommandId(ValueObject):
    value: str


@dataclass(frozen=True)
class Topic(ValueObject):
    value: str

    def extract_device_id(self) -> str:
        parts = self.value.split("/")
        return parts[3]