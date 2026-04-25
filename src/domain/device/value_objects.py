# src/domain/device/value_objects.py
from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceId:
    value: str


@dataclass(frozen=True)
class Topic:
    value: str

    def extract_device_id(self) -> str:
        parts = self.value.split("/")
        return parts[3]