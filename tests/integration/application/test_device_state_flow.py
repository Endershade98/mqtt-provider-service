# tests/integration/application/test_device_state_flow.py

import pytest

from src.application.use_cases.update_device_state import UpdateDeviceStateUseCase
from src.application.use_cases.dto.update_device_state_dto import UpdateDeviceStateDTO

from src.infrastructure.persistence.django.repositories.device_repository import DjangoDeviceRepository
from src.infrastructure.persistence.django.repositories.outbox_repository import DjangoOutboxRepository
from src.infrastructure.persistence.django.unit_of_work import DjangoUnitOfWork

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId, DeviceStatus


@pytest.mark.django_db
def test_update_device_state_flow():
    repo = DjangoDeviceRepository()
    outbox = DjangoOutboxRepository()
    uow = DjangoUnitOfWork()

    device = Device(
        id=DeviceId("dev-1"),
        name="Sensor",
        device_type="temp",
        organization="acme",
    )

    repo.save(device)

    use_case = UpdateDeviceStateUseCase(repo, uow, outbox)

    dto = UpdateDeviceStateDTO(
        device_id="dev-1",
        target_status=DeviceStatus.OFFLINE,
    )

    use_case.execute(dto)

    updated = repo.get(DeviceId("dev-1"))

    assert updated.status == DeviceStatus.OFFLINE