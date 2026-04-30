# tests/unit/application/test_handle_telemetry.py
from unittest.mock import Mock
import pytest

from src.application.use_cases.handle_telemetry import (
    HandleTelemetryUseCase,
    HandleTelemetryInput,
)

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId
from django.utils import timezone

now = timezone.now()

def make_device():
    device = Mock(spec=Device)
    device.id = DeviceId("dev-1")
    device.pull_events.return_value = []
    return device


def make_input():
    return HandleTelemetryInput(
        device_id=DeviceId("dev-1"),  # ✅ FIX: Value Object
        payload={"t": 1},
        received_at=now
    )


# =========================
# HAPPY PATH
# =========================

def test_handle_telemetry_happy_path_generates_events_and_calls_outbox():

    device_repo = Mock()
    telemetry_repo = Mock()
    outbox_repo = Mock()

    device = make_device()
    device.pull_events.return_value = ["DeviceBecameOnline"]

    device_repo.get.return_value = device

    use_case = HandleTelemetryUseCase(
        device_repo,
        telemetry_repo,
        outbox_repo
    )

    events = use_case.execute(make_input())

    assert events == ["DeviceBecameOnline"]

    device_repo.get.assert_called_once_with(DeviceId("dev-1"))
    device_repo.save.assert_called_once_with(device)

    telemetry_repo.save.assert_called_once()

    outbox_repo.save.assert_called_once_with(["DeviceBecameOnline"])


# =========================
# NO EVENTS
# =========================

def test_handle_telemetry_no_events_does_not_call_outbox():

    device_repo = Mock()
    telemetry_repo = Mock()
    outbox_repo = Mock()

    device = make_device()
    device.pull_events.return_value = []

    device_repo.get.return_value = device

    use_case = HandleTelemetryUseCase(
        device_repo,
        telemetry_repo,
        outbox_repo
    )

    events = use_case.execute(make_input())

    assert events == []

    telemetry_repo.save.assert_called_once()
    device_repo.save.assert_called_once_with(device)

    outbox_repo.save.assert_not_called()


# =========================
# DEVICE NOT FOUND
# =========================

def test_handle_telemetry_device_not_found():

    device_repo = Mock()
    telemetry_repo = Mock()
    outbox_repo = Mock()

    device_repo.get.side_effect = Exception("not found")

    use_case = HandleTelemetryUseCase(
        device_repo,
        telemetry_repo,
        outbox_repo
    )

    with pytest.raises(Exception):
        use_case.execute(make_input())

    telemetry_repo.save.assert_not_called()
    outbox_repo.save.assert_not_called()


# =========================
# ALWAYS PERSISTS DEVICE
# =========================

def test_handle_telemetry_always_persists_device():

    device_repo = Mock()
    telemetry_repo = Mock()
    outbox_repo = Mock()

    device = make_device()
    device_repo.get.return_value = device

    use_case = HandleTelemetryUseCase(
        device_repo,
        telemetry_repo,
        outbox_repo
    )

    use_case.execute(make_input())

    device_repo.save.assert_called_once_with(device)


# =========================
# TELEMETRY IS ALWAYS SAVED
# =========================

def test_handle_telemetry_always_saves_telemetry():

    device_repo = Mock()
    telemetry_repo = Mock()
    outbox_repo = Mock()

    device = make_device()
    device_repo.get.return_value = device

    use_case = HandleTelemetryUseCase(
        device_repo,
        telemetry_repo,
        outbox_repo
    )

    use_case.execute(make_input())

    telemetry_repo.save.assert_called_once()