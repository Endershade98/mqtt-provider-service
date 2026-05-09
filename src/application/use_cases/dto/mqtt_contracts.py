# src/application/use_cases/dto/mqtt_contracts.py

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class TelemetryContract:
    device_id: str
    payload: dict[str, Any]
    received_at: datetime


@dataclass(frozen=True)
class AckContract:
    command_id: str