# tests/unit/domain/device/test_device.py

from datetime import datetime, timezone, timedelta

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId, DeviceStatus


def make_device():
    return Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org",
    )


def test_device_initial_state():
    device = make_device()

    assert device.status == DeviceStatus.UNKNOWN
    assert device.last_seen is None
    assert device.is_active is True


def test_device_becomes_online_on_heartbeat():
    device = make_device()

    now = datetime.now(timezone.utc)
    device.record_heartbeat(now)

    assert device.status == DeviceStatus.ONLINE
    assert device.last_seen == now

    events = device.pull_events()
    assert len(events) == 1
    assert events[0].device_id == "dev-1"
    assert events[0].occurred_at == now


def test_device_does_not_duplicate_online_event():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)
    device.pull_events()

    device.record_heartbeat(now + timedelta(seconds=10))

    events = device.pull_events()

    # nessun nuovo evento se già ONLINE
    assert len(events) == 0


def test_device_goes_offline():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)
    device.pull_events()

    device.mark_offline(now)

    assert device.status == DeviceStatus.OFFLINE

    events = device.pull_events()
    assert len(events) == 1
    assert events[0].device_id == "dev-1"


def test_device_offline_is_idempotent():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.mark_offline(now)
    device.mark_offline(now)

    events = device.pull_events()

    assert len(events) == 1  # solo primo evento


def test_device_check_stale_transitions():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)
    device.pull_events()

    later = now + timedelta(seconds=500)

    device.check_stale(later, threshold_seconds=100)

    assert device.status == DeviceStatus.STALE

    events = device.pull_events()
    assert len(events) == 1


def test_device_not_marked_stale_if_recent():
    device = make_device()

    now = datetime.now(timezone.utc)

    device.record_heartbeat(now)
    device.pull_events()

    later = now + timedelta(seconds=10)

    device.check_stale(later, threshold_seconds=100)

    assert device.status == DeviceStatus.ONLINE
    assert len(device.pull_events()) == 0