# tests/unit/application/test_event_contract.py
from datetime import datetime
from unittest.mock import Mock

from src.application.use_cases.handle_telemetry import HandleTelemetryInput, HandleTelemetryUseCase
from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


def test_handle_telemetry_emits_correct_event():

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

    assert any(e.__class__.__name__ == "DeviceBecameOnline" for e in events)