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
from src.domain.shared.events import DomainEvent


@dataclass
class Device:
    id: DeviceId
    name: str
    device_type: str
    organization: str

    is_active: bool = True
    is_online: bool = False
    last_seen: Optional[datetime] = None

    firmware_version: Optional[str] = None
    _events: List[DomainEvent] = field(default_factory=list, init=False)

    # ==========================================
    # DOMAIN BEHAVIOR
    # ==========================================

    def mark_online(self, now: datetime):
        # sempre aggiorniamo last_seen (importantissimo)
        self.last_seen = now

        if not self.is_online:
            self.is_online = True

            self._events.append(
                DeviceBecameOnline(device_id=self.id.value)
            )

    def mark_offline(self):
        if not self.is_online:
            return

        self.is_online = False

        self._events.append(
            DeviceBecameOffline(device_id=self.id.value)
        )

    def check_stale(self, now: datetime, threshold_seconds: int):
        """
        Determina se il device è diventato stale.
        NON forza lo stato, ma lo deriva.
        """
        if not self.last_seen:
            return

        delta = (now - self.last_seen).total_seconds()

        if delta <= threshold_seconds:
            return

        # evita duplicati
        if not self.is_online:
            return

        self.is_online = False

        self._events.append(
            DeviceMarkedStale(device_id=self.id.value)
        )

    def update_firmware(self, version: str):
        self.firmware_version = version

    def pull_events(self) -> List[DomainEvent]:
        events = self._events[:]
        self._events.clear()
        return events