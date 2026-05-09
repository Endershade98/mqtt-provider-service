# tests/unit/domain/device/test_device_state_transitions.py

from datetime import datetime, timezone

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId, DeviceStatus


def make_device():
    return Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org",
    )


def test_online_state_transition():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)

    assert device.status == DeviceStatus.ONLINE


def test_offline_state_transition():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)
    device.mark_offline(now)

    assert device.status == DeviceStatus.OFFLINE


def test_stale_state_transition():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)
    device.check_stale(now, threshold_seconds=0)

    assert device.status == DeviceStatus.STALE