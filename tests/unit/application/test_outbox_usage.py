# tests/unit/application/test_outbox_usage.py
from unittest.mock import Mock
from datetime import datetime

from src.application.use_cases.handle_telemetry import (
    HandleTelemetryUseCase,
    HandleTelemetryInput
)
from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


def test_outbox_is_called_with_events():

    repo = Mock()
    outbox = Mock()

    device = Device(
        id=DeviceId("dev-1"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    repo.get.return_value = device

    use_case = HandleTelemetryUseCase(repo, outbox)

    input_data = HandleTelemetryInput(
        device_id="dev-1",
        payload={"t": 1},
        received_at=datetime(2024,1,1,12,0,0)
    )

    use_case.execute(input_data)

    assert outbox.save.called is True
    args = outbox.save.call_args[0][0]

    assert len(args) == 1

def test_use_case_saves_events_to_outbox():

    repo = Mock()
    outbox = Mock()

    device = Device(
        id=DeviceId("dev-1"),
        name="test",
        device_type="sensor",
        organization="org"
    )

    repo.get.return_value = device

    uc = HandleTelemetryUseCase(repo, outbox)

    events = uc.execute(HandleTelemetryInput(
        device_id="dev-1",
        payload={},
        received_at=datetime(2024,1,1)
    ))

    outbox.save.assert_called()
    repo.save.assert_called_once()
    assert len(events) >= 0