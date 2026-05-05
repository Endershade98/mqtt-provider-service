# src/domain/device/value_objects.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from src.domain.device.value_objects import DeviceId, DeviceStatus
from src.domain.device.events import (
    DeviceBecameOnline,
    DeviceBecameOffline,
    DeviceMarkedStale,
)


@dataclass
class Device:
    id: DeviceId
    name: str
    device_type: str
    organization: str

    status: DeviceStatus = DeviceStatus.UNKNOWN
    is_active: bool = True
    last_seen: Optional[datetime] = None
    firmware_version: Optional[str] = None

    _events: List = field(default_factory=list, init=False)

    # =============================
    # DOMAIN BEHAVIOR
    # =============================

    def mark_online(self, now: datetime):
        self.last_seen = now

        if self.status == DeviceStatus.ONLINE:
            return

        self.status = DeviceStatus.ONLINE

        self._events.append(
            DeviceBecameOnline(
                device_id=self.id.value,
                occurred_at=now
            )
        )

    def mark_offline(self, now: datetime):
        if self.status == DeviceStatus.OFFLINE:
            return

        self.status = DeviceStatus.OFFLINE

        self._events.append(
            DeviceBecameOffline(
                device_id=self.id.value,
                occurred_at=now
            )
        )

    def mark_stale(self, now: datetime):
        if self.status == DeviceStatus.STALE:
            return

        self.status = DeviceStatus.STALE

        self._events.append(
            DeviceMarkedStale(
                device_id=self.id.value,
                occurred_at=now
            )
        )

    def check_stale(self, now: datetime, threshold_seconds: int):
        if not self.last_seen:
            return

        if self.status != DeviceStatus.ONLINE:
            return

        delta = (now - self.last_seen).total_seconds()

        if delta > threshold_seconds:
            self.mark_stale(now)

    def update_last_seen(self, timestamp: datetime):
        self.last_seen = timestamp

    def update_firmware(self, version: str):
        self.firmware_version = version

    def pull_events(self):
        events = self._events[:]
        self._events.clear()
        return events