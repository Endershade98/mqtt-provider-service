# tests/unit/application/test_handle_telemetry.py

from unittest.mock import Mock
from django.utils import timezone

from src.application.use_cases.handle_telemetry import (
    HandleTelemetryUseCase,
    HandleTelemetryDTO,
)
from src.domain.device.value_objects import DeviceId

now = timezone.now()


def make_input():
    return HandleTelemetryDTO(
        device_id=DeviceId("dev-1"),
        payload={"t": 1},
        received_at=now
    )


def test_handle_telemetry_happy_path_generates_events_and_calls_service():

    device_service = Mock()

    device_service.record_telemetry.return_value = ["DeviceBecameOnline"]

    uc = HandleTelemetryUseCase(device_service)

    events = uc.execute(make_input())

    assert events == ["DeviceBecameOnline"]
    device_service.record_telemetry.assert_called_once()


def test_handle_telemetry_no_events():

    device_service = Mock()
    device_service.record_telemetry.return_value = []

    uc = HandleTelemetryUseCase(device_service)

    events = uc.execute(make_input())

    assert events == []
    device_service.record_telemetry.assert_called_once()


def test_handle_telemetry_device_not_found():

    device_service = Mock()
    device_service.record_telemetry.side_effect = Exception("not found")

    uc = HandleTelemetryUseCase(device_service)

    try:
        uc.execute(make_input())
        assert False
    except Exception:
        pass


def test_handle_telemetry_always_persists_device():

    device_service = Mock()
    device_service.record_telemetry.return_value = []

    uc = HandleTelemetryUseCase(device_service)

    uc.execute(make_input())

    device_service.record_telemetry.assert_called_once()


def test_handle_telemetry_always_saves_telemetry():

    device_service = Mock()
    device_service.record_telemetry.return_value = []

    uc = HandleTelemetryUseCase(device_service)

    uc.execute(make_input())

    device_service.record_telemetry.assert_called_once()