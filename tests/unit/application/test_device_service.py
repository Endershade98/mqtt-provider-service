# tests/unit/application/test_device_service.py

from django.utils import timezone
from datetime import datetime

from src.application.services.device_service import DeviceService

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId
from src.domain.telemetry.entity import Telemetry

date = timezone.make_aware(datetime(2024, 1, 1, 12, 0, 0))


def test_record_telemetry_triggers_online_event():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    telemetry = Telemetry(
        device_id=device.id,
        payload={"t": 1},
        received_at=date
    )

    service = DeviceService()

    service.record_telemetry(device, telemetry)

    events = device.pull_events()

    assert len(events) == 1
    assert events[0].__class__.__name__ == "DeviceBecameOnline"