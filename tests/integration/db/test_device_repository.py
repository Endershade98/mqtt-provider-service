# tests/integration/db/test_device_repository.py
import pytest

from django.core.exceptions import ObjectDoesNotExist

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId
from src.infrastructure.persistence.django.repositories.device_repository import DjangoDeviceRepository
from src.infrastructure.persistence.django.models import DeviceModel


@pytest.mark.django_db
def test_device_repository_roundtrip():

    repo = DjangoDeviceRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org"
    )

    repo.save(device)  # ✅ SOLO persistence

    loaded = repo.get(DeviceId("dev-1"))

    assert loaded.id.value == "dev-1"
    assert loaded.name == "sensor"
    assert DeviceModel.objects.count() == 1

def test_device_update_overwrites_fields():
    repo = DjangoDeviceRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="old",
        device_type="iot",
        organization="org"
    )

    repo.save(device)

    device.name = "new"
    repo.save(device)

    loaded = repo.get(DeviceId("dev-1"))

    assert loaded.name == "new"
    assert DeviceModel.objects.count() == 1

def test_device_optional_fields_persistence():
    repo = DjangoDeviceRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org",
        firmware_version=None
    )

    repo.save(device)

    model = DeviceModel.objects.get(id="dev-1")
    assert model.firmware_version is None

def test_device_get_not_found():
    repo = DjangoDeviceRepository()

    with pytest.raises(ObjectDoesNotExist):
        repo.get(DeviceId("missing"))