# tests/unit/domain/telemetry/test_telemetry_device_integration.py
import pytest
from datetime import timedelta
from django.utils import timezone
from src.application.services.device_service import DeviceService
from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId
from src.domain.telemetry.entity import Telemetry
from src.domain.telemetry.events import TelemetryReceived

service = DeviceService()


def test_telemetry_marks_device_online():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456"
    )

    telemetry = Telemetry(
        device_id=device.id,
        payload={"temperature": 22.5},
        received_at=timezone.now()
    )

    service.record_telemetry(device, telemetry)

    assert device.is_online is True
    assert device.last_seen == telemetry.received_at

def test_multiple_telemetry_no_duplicate_online_event():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456"
    )

    now = timezone.now()

    telemetry1 = Telemetry(
        device_id=device.id,
        payload={"temperature": 22.5},
        received_at=now
    )

    telemetry2 = Telemetry(
        device_id=device.id,
        payload={"temperature": 23.0},
        received_at=now + timedelta(minutes=1)
    )

    service.record_telemetry(device, telemetry1)
    service.record_telemetry(device, telemetry2)

    assert device.is_online is True
    assert device.last_seen == telemetry2.received_at


