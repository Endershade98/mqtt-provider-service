# tests/unit/application/test_event_contract.py

from django.utils import timezone
from unittest.mock import Mock

from src.application.use_cases.handle_telemetry import (
    HandleTelemetryUseCase,
    HandleTelemetryDTO
)
from src.domain.device.value_objects import DeviceId

now = timezone.now()


def test_handle_telemetry_emits_correct_event():

    device_service = Mock()

    uc = HandleTelemetryUseCase(device_service)

    dto = HandleTelemetryDTO(
        device_id=DeviceId("dev-1"),
        payload={"temp": 1},
        received_at=now
    )

    device_service.record_telemetry.return_value = ["DeviceBecameOnline"]

    events = uc.execute(dto)

    assert events == ["DeviceBecameOnline"]
    device_service.record_telemetry.assert_called_once_with(dto)