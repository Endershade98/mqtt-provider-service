# tests/unit/application/test_event_contract.py

from unittest.mock import Mock

from src.application.use_cases.handle_telemetry import (
    HandleTelemetryInput,
    HandleTelemetryUseCase
)
from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId
from django.utils import timezone

now = timezone.now()


def test_handle_telemetry_emits_correct_event():

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

    device_telemetry_input = HandleTelemetryInput(
        device_id=device.id,
        payload={"temp": 1},
        received_at=now
    )

    events = uc.execute(device_telemetry_input)

    
