# tests/integration/application/test_telemetry_flow.py

import pytest
from datetime import datetime

from src.application.use_cases.handle_telemetry import HandleTelemetryUseCase
from src.application.use_cases.dto.handle_telemetry_dto import HandleTelemetryDTO

from src.infrastructure.persistence.django.repositories.device_repository import DjangoDeviceRepository
from src.infrastructure.persistence.django.repositories.telemetry_repository import DjangoTelemetryRepository
from src.infrastructure.persistence.django.repositories.outbox_repository import DjangoOutboxRepository
from src.infrastructure.persistence.django.unit_of_work import DjangoUnitOfWork

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


@pytest.mark.django_db
def test_handle_telemetry_flow():
    device_repo = DjangoDeviceRepository()
    telemetry_repo = DjangoTelemetryRepository()
    outbox = DjangoOutboxRepository()
    uow = DjangoUnitOfWork()

    device = Device(
        id=DeviceId("dev-1"),
        name="Sensor",
        device_type="temp",
        organization="acme",
    )

    device_repo.save(device)

    use_case = HandleTelemetryUseCase(
        device_repo,
        telemetry_repo,
        uow,
        outbox,
    )

    dto = HandleTelemetryDTO(
        device_id="dev-1",
        payload={"temperature": 25},
        received_at=datetime.utcnow(),
    )

    use_case.execute(dto)

    saved = device_repo.get(DeviceId("dev-1"))

    assert saved.status.value == "ONLINE"