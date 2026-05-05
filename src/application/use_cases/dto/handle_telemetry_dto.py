# src/application/use_cases/dto/handle_telemetry_dto.py

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HandleTelemetryDTO:
    device_id: str
    payload: dict
    received_at: datetime