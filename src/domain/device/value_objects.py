# src/domain/device/value_objects.py

from dataclasses import dataclass

from src.domain.shared.value_objects import ValueObject
from src.domain.shared.exceptions import InvalidDeviceId

@dataclass(frozen=True)
class DeviceId(ValueObject):
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or not self.value.strip():
            raise InvalidDeviceId("DeviceId cannot be empty")