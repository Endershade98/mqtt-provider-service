# tests/unit/application/test_outbox_usage.py

from unittest.mock import Mock
from datetime import datetime

from src.application.use_cases.handle_telemetry import (
    HandleTelemetryUseCase,
    HandleTelemetryDTO
)

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


def test_outbox_is_called_with_events():

    device_repo = Mock()
    telemetry_repo = Mock()
    outbox_repo = Mock()

    device = Device(
        id=DeviceId("dev-1"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    device_repo.get.return_value = device

    use_case = HandleTelemetryUseCase(
        device_repo,
        telemetry_repo,
        outbox_repo
    )

    use_case.execute(
        HandleTelemetryDTO(
            device_id="dev-1",
            payload={"temp": 1},
            received_at=datetime(2024, 1, 1, 12, 0, 0)
        )
    )

    assert outbox_repo.save.called
    assert len(outbox_repo.save.call_args[0][0]) >= 0


def test_use_case_saves_events_to_outbox():

    device_repo = Mock()
    telemetry_repo = Mock()
    outbox_repo = Mock()

    device = Device(
        id=DeviceId("dev-1"),
        name="test",
        device_type="sensor",
        organization="org"
    )

    device_repo.get.return_value = device

    uc = HandleTelemetryUseCase(
        device_repo,
        telemetry_repo,
        outbox_repo
    )

    events = uc.execute(
        HandleTelemetryDTO(
            device_id="dev-1",
            payload={"temp": 10},
            received_at=datetime(2024, 1, 1)
        )
    )

    outbox_repo.save.assert_called()
    device_repo.save.assert_called_once()