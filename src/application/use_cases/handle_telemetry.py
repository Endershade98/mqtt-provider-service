# src/application/use_cases/handle_telemetry.py

from dataclasses import dataclass
from datetime import datetime

from src.domain.telemetry.entity import Telemetry
from src.domain.device.value_objects import DeviceId


# =========================
# INPUT DTO
# =========================

@dataclass
class HandleTelemetryInput:
    device_id: DeviceId
    payload: dict
    received_at: datetime


# =========================
# USE CASE
# =========================

class HandleTelemetryUseCase:

    def __init__(self, device_repository, telemetry_repository, outbox_repository):
        self.device_repository = device_repository
        self.telemetry_repository = telemetry_repository
        self.outbox_repository = outbox_repository

    def execute(self, input_dto: HandleTelemetryInput):

        # 1. Load aggregate
        device = self.device_repository.get(input_dto.device_id)

        # 2. Domain behavior
        device.update_last_seen(input_dto.received_at)

        # 3. Create telemetry entity (DOMAIN)
        telemetry = Telemetry(
            device_id=device.id,
            payload=input_dto.payload,
            received_at=input_dto.received_at
        )

        # 4. Persist telemetry
        self.telemetry_repository.save(telemetry)

        # 5. Collect domain events
        events = device.pull_events()

        # 6. Persist device state
        self.device_repository.save(device)

        # 7. Outbox
        if events:
            self.outbox_repository.save(events)

        return events