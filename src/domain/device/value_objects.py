# src/domain/device/value_objects.py
from dataclasses import dataclass
from src.domain.shared.value_objects import ValueObject
from src.domain.shared.exceptions import InvalidDeviceId, InvalidTopicFormat

@dataclass(frozen=True)
class DeviceId(ValueObject):
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or not self.value.strip():
            raise InvalidDeviceId("DeviceId cannot be empty")

@dataclass(frozen=True)
class CommandId(ValueObject):
    value: str


@dataclass(frozen=True)
class Topic(ValueObject):
    value: str

    def extract_device_id(self) -> str:
        parts = self.value.split("/")

        if len(parts) < 5:
            raise InvalidTopicFormat(self.value)

        return parts[3]