# tests/integration/infrastructure/persistence/test_device_repository.py

import pytest

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId
from src.infrastructure.persistence.django.repositories.device_repository import DjangoDeviceRepository


@pytest.mark.django_db
def test_device_repository_roundtrip():

    repo = DjangoDeviceRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org"
    )

    repo.save(device)

    loaded = repo.get(DeviceId("dev-1"))

    assert loaded.id.value == "dev-1"
    assert loaded.name == "sensor"
    assert loaded.device_type == "iot"