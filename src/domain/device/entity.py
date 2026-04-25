# src/domain/device/entity.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Device:
    id: str
    name: str
    device_type: str
    organization: str

    is_active: bool = True
    is_online: bool = False
    last_seen: Optional[datetime] = None

    firmware_version: Optional[str] = None

    def mark_online(self, timestamp: datetime):
        self.is_online = True
        self.last_seen = timestamp

    def mark_offline(self):
        self.is_online = False

    def update_firmware(self, version: str):
        self.firmware_version = version