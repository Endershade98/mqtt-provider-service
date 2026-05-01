# src/domain/device/entity.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from src.domain.device.value_objects import DeviceId
from src.domain.device.events import (
    DeviceBecameOnline,
    DeviceBecameOffline,
    DeviceMarkedStale,
)


@dataclass(frozen=True)
class Device:
    id: DeviceId
    name: str
    device_type: str
    organization: str

    is_active: bool = True
    is_online: bool = False
    last_seen: Optional[datetime] = None

    firmware_version: Optional[str] = None
    _events: List = field(default_factory=list, init=False)

    # ==========================================
    # DOMAIN BEHAVIOR
    # ==========================================

    def mark_online(self, now: datetime):

        self.last_seen = now

        if self.is_online:
            return

        self.is_online = True

        self._events.append(
            DeviceBecameOnline(
                device_id=self.id.value,
                occurred_at=now
            )
        )

    def mark_offline(self, now: datetime):

        if not self.is_online:
            return

        self.is_online = False

        self._events.append(
            DeviceBecameOffline(
                device_id=self.id.value,
                occurred_at=now
            )
        )

    def check_stale(self, now: datetime, threshold_seconds: int):

        if not self.last_seen:
            return

        if not self.is_online:
            return

        delta = (now - self.last_seen).total_seconds()

        if delta <= threshold_seconds:
            return

        self.is_online = False

        self._events.append(
            DeviceMarkedStale(
                device_id=self.id.value,
                occurred_at=now
            )
        )

    def update_firmware(self, version: str):
        self.firmware_version = version

    def pull_events(self) -> List:
        events = self._events[:]
        self._events.clear()
        return events

    def update_last_seen(self, timestamp: datetime):
        """
        Domain behavior:
        update device heartbeat timestamp
        """
        self.last_seen = timestamp

        self._events.append(
            DeviceBecameOnline(
                device_id=self.id.value,
                occurred_at=timestamp
            )
        )