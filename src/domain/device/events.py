# src/domain/device/events.py
from dataclasses import dataclass
from src.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class DeviceBecameOnline(DomainEvent):
    device_id: str

@dataclass(frozen=True)
class DeviceBecameOffline(DomainEvent):
    device_id: str

@dataclass(frozen=True)
class DeviceMarkedStale(DomainEvent):
    device_id: str