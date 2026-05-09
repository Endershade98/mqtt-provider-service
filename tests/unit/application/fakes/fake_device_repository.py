# tests/unit/application/fakes/fake_device_repository.py

from src.domain.device.value_objects import DeviceId


class FakeDeviceRepository:
    def __init__(self):
        self.storage = {}

    def save(self, device):
        self.storage[device.id.value] = device

    def get(self, device_id: DeviceId):
        return self.storage.get(device_id.value)