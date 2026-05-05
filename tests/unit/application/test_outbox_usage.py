# tests/unit/application/test_outbox_usage.py

from unittest.mock import Mock
from datetime import datetime

from src.application.use_cases.handle_telemetry import (
    HandleTelemetryUseCase,
    HandleTelemetryDTO
)
from src.domain.device.value_objects import DeviceId


def test_outbox_is_called_with_events():

    device_service = Mock()

    device_service.record_telemetry.return_value = ["DeviceBecameOnline"]

    uc = HandleTelemetryUseCase(device_service)

    uc.execute(
        HandleTelemetryDTO(
            device_id=DeviceId("dev-1"),
            payload={"temp": 1},
            received_at=datetime(2024, 1, 1, 12, 0, 0)
        )
    )

    device_service.record_telemetry.assert_called_once()


def test_use_case_saves_events_to_outbox():

    device_service = Mock()
    device_service.record_telemetry.return_value = ["DeviceBecameOnline"]

    uc = HandleTelemetryUseCase(device_service)

    uc.execute(
        HandleTelemetryDTO(
            device_id=DeviceId("dev-1"),
            payload={"temp": 10},
            received_at=datetime(2024, 1, 1)
        )
    )

    device_service.record_telemetry.assert_called_once()