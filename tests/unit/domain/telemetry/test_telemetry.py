# tests/unit/domain/telemetry/test_telemetry.py

from datetime import datetime
from django.utils import timezone

from src.domain.telemetry.entity import Telemetry
from src.domain.device.value_objects import DeviceId


now = timezone.make_aware(datetime(2024, 1, 1, 12, 0, 0))


def test_telemetry_is_valid():
    telemetry = Telemetry(
        device_id=DeviceId("dev-1"),
        payload={"temp": 22},
        received_at=now
    )

    assert telemetry.payload == {"temp": 22}


def test_empty_payload_invalid():
    import pytest
    from src.domain.shared.exceptions import TelemetryValidationError

    with pytest.raises(TelemetryValidationError):
        Telemetry(
            device_id=DeviceId("dev-1"),
            payload={},
            received_at=now
        )