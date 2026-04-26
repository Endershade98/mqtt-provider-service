# src/domain/device/events.py
from dataclasses import dataclass
import datetime



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