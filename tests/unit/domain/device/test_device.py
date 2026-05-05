# tests/unit/domain/device/test_device.py

from datetime import datetime, timedelta, timezone

from src.domain.device.entity import Device
from src.domain.device.events import (
    DeviceBecameOnline,
    DeviceBecameOffline,
    DeviceMarkedStale,
)
from src.domain.device.value_objects import DeviceId, DeviceStatus


date = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def make_device():
    return Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org"
    )


# ----------------------------------
# ONLINE
# ----------------------------------

def test_mark_online_changes_status_and_emits_event():
    device = make_device()

    device.mark_online(date)

    events = device.pull_events()

    assert device.status == DeviceStatus.ONLINE
    assert device.last_seen == date
    assert len(events) == 1
    assert isinstance(events[0], DeviceBecameOnline)


def test_mark_online_is_idempotent():
    device = make_device()

    device.mark_online(date)
    device.mark_online(date)

    events = device.pull_events()

    assert len(events) == 1


# ----------------------------------
# OFFLINE
# ----------------------------------

def test_mark_offline_changes_status():
    device = make_device()

    device.mark_online(date)
    device.pull_events()

    device.mark_offline(date)

    events = device.pull_events()

    assert device.status == DeviceStatus.OFFLINE
    assert len(events) == 1
    assert isinstance(events[0], DeviceBecameOffline)


# ----------------------------------
# STALE
# ----------------------------------

def test_check_stale_marks_device_stale():
    device = make_device()

    device.mark_online(date)
    device.pull_events()

    now = date + timedelta(minutes=10)

    device.check_stale(now, threshold_seconds=300)

    events = device.pull_events()

    assert device.status == DeviceStatus.STALE
    assert len(events) == 1
    assert isinstance(events[0], DeviceMarkedStale)


def test_check_stale_does_nothing_if_recent():
    device = make_device()

    device.mark_online(date)
    device.pull_events()

    now = date + timedelta(minutes=2)

    device.check_stale(now, threshold_seconds=300)

    assert device.status == DeviceStatus.ONLINE
    assert device.pull_events() == []