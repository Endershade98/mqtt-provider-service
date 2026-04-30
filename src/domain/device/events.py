# src/domain/device/events.py
from dataclasses import dataclass
from datetime import datetime
from src.domain.device.value_objects import DeviceId


@dataclass
class DeviceMarkedOnline:
    device_id: DeviceId
    timestamp: datetime

@dataclass(frozen=True)
class DeviceBecameOnline:
    device_id: str
    occurred_at: datetime


@dataclass(frozen=True)
class DeviceBecameOffline:
    device_id: str
    occurred_at: datetime

@dataclass(frozen=True)
class DeviceMarkedStale:
    device_id: str
    occurred_at: datetime