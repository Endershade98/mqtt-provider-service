# src/application/use_cases/handle_telemetry.py

from dataclasses import dataclass
from datetime import datetime

from src.domain.device.value_objects import DeviceId


# =========================
# INPUT DTO
# =========================

@dataclass
class HandleTelemetryInput:
    device_id: str
    payload: dict
    received_at: datetime


# =========================
# USE CASE
# =========================

class HandleTelemetryUseCase:

    def __init__(self, device_repository, outbox_repository):
        self.device_repository = device_repository
        self.outbox_repository = outbox_repository

    def execute(self, input_dto: HandleTelemetryInput):
        # 1. Load aggregate
        device = self.device_repository.get(DeviceId(input_dto.device_id))

        # 2. Apply domain logic
        device.mark_online(input_dto.received_at)

        # 3. Collect domain events
        events = device.pull_events()

        # 4. Persist state
        self.device_repository.save(device)

        # 5. Persist events (outbox pattern)
        if events:
            self.outbox_repository.save(events)

        # 6. Return events (optional, useful for tests / orchestration)
        return events