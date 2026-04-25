# src/domain/telemetry/events.py
from dataclasses import dataclass
from src.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class TelemetryReceived(DomainEvent):
    device_id: str