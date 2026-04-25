# src/domain/telemetry/entity.py
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Telemetry:
    device_id: str
    payload: dict
    received_at: datetime
