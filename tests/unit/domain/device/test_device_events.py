# tests/unit/domain/device/test_device_events.py
from datetime import datetime

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


def test_device_emits_online_event():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    now = datetime(2024, 1, 1, 12, 0, 0)

    device.mark_online(now)

    events = device.pull_events()

    assert len(events) == 1

    event = events[0]

    assert event.__class__.__name__ == "DeviceBecameOnline"
    assert event.device_id == "dev-123"


def test_mark_online_emits_event_only_once():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    now = datetime(2024, 1, 1, 12, 0, 0)

    device.mark_online(now)
    device.mark_online(now)

    events = device.pull_events()

    assert len(events) == 1


def test_device_emits_offline_event():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    device.mark_online(datetime(2024, 1, 1, 12, 0, 0))
    device.pull_events()  # reset

    device.mark_offline(now=datetime(2024, 1, 1, 12, 10, 0))

    events = device.pull_events()

    assert len(events) == 1
    assert events[0].__class__.__name__ == "DeviceBecameOffline"


def test_device_emits_stale_event():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    device.mark_online(datetime(2024, 1, 1, 12, 0, 0))
    device.pull_events()  # reset

    device.check_stale(
        now=datetime(2024, 1, 1, 12, 10, 0),
        threshold_seconds=300
    )

    events = device.pull_events()

    assert len(events) == 1
    assert events[0].__class__.__name__ == "DeviceMarkedStale"