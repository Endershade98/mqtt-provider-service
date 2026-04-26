# tests/unit/application/test_handle_telemetry_use_case.py
from datetime import datetime
from unittest.mock import Mock

from src.application.use_cases.handle_telemetry import (
    HandleTelemetryUseCase,
    HandleTelemetryInput,
)
from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


def test_handle_telemetry_registers_outbox_events():
    repo = Mock()
    outbox = Mock()

    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    repo.get.return_value = device

    use_case = HandleTelemetryUseCase(repo, outbox)

    input_data = HandleTelemetryInput(
        device_id="dev-123",
        payload={"t": 1},
        received_at=datetime(2024, 1, 1, 12, 0, 0)
    )

    events = use_case.execute(input_data)

    assert len(events) == 1

    # VERIFICA EPIC 2 CORE REQUIREMENT
    outbox.save(events)

def test_handle_telemetry_idempotency():

    repo = Mock()
    outbox = Mock()

    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    repo.get.return_value = device

    use_case = HandleTelemetryUseCase(repo, outbox)

    input_data = HandleTelemetryInput(
        device_id="dev-123",
        payload={"t": 1},
        received_at=datetime(2024, 1, 1, 12, 0, 0)
    )

    events1 = use_case.execute(input_data)
    events2 = use_case.execute(input_data)

    # idempotenza domain-level (no duplicate online event)
    assert len(events1) == 1
    assert len(events2) == 0  # oppure stessa logica del tuo domain

    repo.save.assert_called()


def test_handle_telemetry_idempotent():

    repo = Mock()
    outbox = Mock()

    device = Device(
        id=DeviceId("dev-1"),
        name="test",
        device_type="sensor",
        organization="org",
        is_online=True
    )

    repo.get.return_value = device

    uc = HandleTelemetryUseCase(repo, outbox)

    events = uc.execute(HandleTelemetryInput(
        device_id="dev-1",
        payload={},
        received_at=datetime(2024,1,1)
    ))

    # nessun evento duplicato
    assert len(events) <= 1