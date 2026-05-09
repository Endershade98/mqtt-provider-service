# src/domain/telemetry/events.py

from dataclasses import dataclass


@dataclass(frozen=True)
class TelemetryReceived:
    device_id: str
    payload: dict