# tests/unit/domain/device/test_device_events.py

from datetime import datetime, timezone, timedelta
from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


def make_device():
    return Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org",
    )


def test_online_event_emitted_on_first_heartbeat():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)

    events = device.pull_events()

    assert len(events) == 1
    assert events[0].__class__.__name__ == "DeviceBecameOnline"


def test_no_event_when_already_online():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)
    device.pull_events()

    device.record_heartbeat(now)

    assert len(device.pull_events()) == 0


def test_offline_event_emitted():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)
    device.pull_events()

    device.mark_offline(now)

    events = device.pull_events()

    assert len(events) == 1
    assert events[0].__class__.__name__ == "DeviceBecameOffline"


def test_stale_event_emitted():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)
    device.pull_events()

    # IMPORTANT: use future time for determinism
    later = now + timedelta(seconds=100)

    device.check_stale(later, threshold_seconds=0)

    events = device.pull_events()

    assert len(events) == 1
    assert events[0].__class__.__name__ == "DeviceMarkedStale"