# tests/integration/infrastructure/persistence/test_telemetry_repository.py

import pytest

from datetime import datetime

from src.domain.telemetry.entity import Telemetry
from src.domain.device.value_objects import DeviceId
from src.infrastructure.persistence.django.repositories.telemetry_repository import DjangoTelemetryRepository


@pytest.mark.django_db
def test_telemetry_repository_persists_and_loads():

    repo = DjangoTelemetryRepository()

    telemetry = Telemetry(
        device_id=DeviceId("dev-1"),
        payload={"temp": 22},
        received_at=datetime.utcnow()
    )

    repo.save(telemetry)

    result = repo.get_all_for_device(DeviceId("dev-1"))

    assert len(result) == 1
    assert result[0].payload["temp"] == 22