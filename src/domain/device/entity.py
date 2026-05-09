# src/domain/device/entity.py

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

    # -----------------------------------
    # TELEMETRY / HEARTBEAT ENTRYPOINT
    # -----------------------------------

    def record_heartbeat(self, now: datetime):
        """
        Telemetry arrived from device.
        Update last_seen.
        If device was not online -> becomes online.
        """
        self.last_seen = now

        if self.status != DeviceStatus.ONLINE:
            self.status = DeviceStatus.ONLINE

            self._events.append(
                DeviceBecameOnline(
                    device_id=self.id.value,
                    occurred_at=now
                )
            )

    # -----------------------------------
    # EXPLICIT DISCONNECT
    # -----------------------------------

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

    # -----------------------------------
    # STALE DETECTION
    # -----------------------------------

    def check_stale(self, now: datetime, threshold_seconds: int):
        if self.status != DeviceStatus.ONLINE:
            return

        if self.last_seen is None:
            return

        delta_seconds = (now - self.last_seen).total_seconds()

        # FIX: include equality edge case (test deterministic)
        if delta_seconds >= threshold_seconds and threshold_seconds >= 0:

            if self.status != DeviceStatus.STALE:
                self.status = DeviceStatus.STALE

                self._events.append(
                    DeviceMarkedStale(
                        device_id=self.id.value,
                        occurred_at=now
                    )
                )

    # -----------------------------------

    def update_firmware(self, version: str):
        self.firmware_version = version

    def pull_events(self):
        events = self._events[:]
        self._events.clear()
        return events