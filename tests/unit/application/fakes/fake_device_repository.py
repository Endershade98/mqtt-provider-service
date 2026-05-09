# tests/unit/application/fakes/fake_device_repository.py

class FakeDeviceRepository:
    def __init__(self):
        self.devices = {}

    def save(self, device):
        self.devices[device.id.value] = device

    def get(self, device_id):
        return self.devices.get(device_id.value)