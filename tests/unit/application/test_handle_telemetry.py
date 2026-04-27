# tests/unit/application/test_handle_telemetry_use_case.py
from unittest.mock import Mock
import pytest

from src.application.use_cases.handle_telemetry import (
    HandleTelemetryUseCase,
    HandleTelemetryInput,
)

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


def test_handle_telemetry_happy_path_generates_events_and_calls_outbox():

    repo = Mock()
    outbox = Mock()

    device = Mock(spec=Device)
    repo.get.return_value = device

    device.pull_events.return_value = ["DeviceBecameOnline"]

    use_case = HandleTelemetryUseCase(repo, outbox)

    events = use_case.execute(
        HandleTelemetryInput(
            device_id="dev-1",
            payload={"t": 1},
            received_at=None
        )
    )

    assert events == ["DeviceBecameOnline"]
    repo.save.assert_called_once_with(device)
    outbox.save.assert_called_once_with(["DeviceBecameOnline"])

def test_handle_telemetry_no_events_does_not_call_outbox():
    repo = Mock()
    outbox = Mock()

    device = Mock(spec=Device)
    repo.get.return_value = device

    device.pull_events.return_value = []

    use_case = HandleTelemetryUseCase(repo, outbox)

    events = use_case.execute(
        HandleTelemetryInput(
            device_id="dev-1",
            payload={},
            received_at=None
        )
    )

    assert events == []
    repo.save.assert_called_once_with(device)
    outbox.save.assert_not_called()

def test_handle_telemetry_device_not_found():

    repo = Mock()
    outbox = Mock()

    repo.get.side_effect = Exception("not found")

    use_case = HandleTelemetryUseCase(repo, outbox)

    with pytest.raises(Exception):
        use_case.execute(
            HandleTelemetryInput(
                device_id="missing",
                payload={},
                received_at=None
            )
        )

def test_handle_telemetry_always_persists_device():

    repo = Mock()
    outbox = Mock()

    device = Mock(spec=Device)
    repo.get.return_value = device

    device.pull_events.return_value = []

    use_case = HandleTelemetryUseCase(repo, outbox)

    use_case.execute(
        HandleTelemetryInput(
            device_id="dev-1",
            payload={},
            received_at=None
        )
    )

    repo.save.assert_called_once_with(device)

