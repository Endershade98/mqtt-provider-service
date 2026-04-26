# src/application/use_cases/handle_telemetry.py
from dataclasses import dataclass
from datetime import datetime

from src.domain.device.value_objects import DeviceId



@dataclass
class HandleTelemetryInput:
    device_id: str
    payload: dict
    received_at: datetime



class HandleTelemetryUseCase:

    def __init__(self, device_repository, outbox):
        self.device_repository = device_repository
        self.outbox = outbox

    def execute(self, input_data: HandleTelemetryInput):

        device = self.device_repository.get(DeviceId(input_data.device_id))

        device.mark_online(input_data.received_at)

        return self._commit(device)

    def _commit(self, device):
        events = device.pull_events()
        self.device_repository.save(device)
        self.outbox.save(events)
        return events