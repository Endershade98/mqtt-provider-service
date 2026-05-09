# src/domain/telemetry/entity.py

from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from src.domain.device.value_objects import DeviceId
from src.domain.shared.exceptions import TelemetryValidationError


@dataclass
class Telemetry:
    device_id: DeviceId
    payload: Dict
    received_at: datetime

    def __post_init__(self):
        if not self.payload:
            raise TelemetryValidationError("Telemetry payload cannot be empty")
    
    def is_empty(self) -> bool:
        return not bool(self.payload)
