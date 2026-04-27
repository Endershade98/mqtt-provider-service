# src/application/use_cases/update_device_state.py
from datetime import datetime
from src.domain.device.value_objects import DeviceId


class UpdateDeviceStateUseCase:

    def __init__(self, device_repository, outbox):
        self.device_repository = device_repository
        self.outbox = outbox

    def execute(self, device_id, is_online):

        device = self.device_repository.get(device_id)

        if is_online:
            device.mark_online(datetime.datetime.now())
        else:
            device.mark_offline(now=datetime.datetime.now())

        events = device.pull_events()

        self.device_repository.save(device)
        self.outbox.save(events)

        return events