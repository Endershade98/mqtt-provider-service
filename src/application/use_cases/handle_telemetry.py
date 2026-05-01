# src/application/use_cases/handle_telemetry.py

from dataclasses import dataclass
from django.db import transaction


@dataclass(frozen=True)
class HandleTelemetryDTO:
    device_id: str
    payload: dict
    received_at: str | None = None


class HandleTelemetryUseCase:

    def __init__(self, device_service):
        self.device_service = device_service

    @transaction.atomic
    def execute(self, dto: HandleTelemetryDTO):

        return self.device_service.process_telemetry(
            device_id=dto.device_id,
            payload=dto.payload,
            received_at=dto.received_at,
        )