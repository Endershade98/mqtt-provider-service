# tests/unit/domain/device/test_device.py
import pytest
from datetime import datetime, timedelta

from src.application.services.device_service import DeviceService
from src.domain.device.entity import Device
from src.domain.device.events import DeviceBecameOnline
from src.domain.device.value_objects import DeviceId
from src.domain.telemetry.entity import Telemetry

service = DeviceService()

# ----------------------------------------
# ONLINE / LAST_SEEN
# ----------------------------------------

def test_mark_online_updates_last_seen():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456"
    )

    now = datetime(2024, 1, 1, 12, 0, 0)

    device.mark_online(now)

    assert device.is_online is True
    assert device.last_seen == now
    assert isinstance(device.pull_events()[0], DeviceBecameOnline)


def test_mark_online_idempotent():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456"
    )

    now = datetime(2024, 1, 1, 12, 0, 0)

    device.mark_online(now)
    device.mark_online(now)

    events = device.pull_events()

    # solo 1 evento online
    assert len(events) == 1
    assert device.is_online is True
    assert isinstance(events[0], DeviceBecameOnline)


# ----------------------------------------
# OFFLINE
# ----------------------------------------

def test_device_goes_offline():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456"
    )

    now = datetime(2024, 1, 1, 12, 0, 0)

    device.mark_online(now)
    device.mark_offline(now)

    assert device.is_online is False

    events = device.pull_events()
    assert any(e.__class__.__name__ == "DeviceBecameOffline" for e in events)


# ----------------------------------------
# STALE LOGIC
# ----------------------------------------

def test_device_not_stale_if_recent():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    device.mark_online(datetime(2024, 1, 1, 12, 0, 0))
    device.pull_events()  # 👈 CLEAN STATE

    now = datetime(2024, 1, 1, 12, 2, 0)

    device.check_stale(now, threshold_seconds=300)

    assert device.is_online is True
    assert device.last_seen == datetime(2024, 1, 1, 12, 0, 0)
    assert isinstance(device.pull_events(), list)
    assert len(device.pull_events()) == 0


def test_device_becomes_stale():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    device.mark_online(datetime(2024, 1, 1, 12, 0, 0))

    now = datetime(2024, 1, 1, 12, 10, 0)

    device.check_stale(now, threshold_seconds=300)

    assert device.is_online is False

    events = device.pull_events()
    assert any(e.__class__.__name__ == "DeviceMarkedStale" for e in events)


# ----------------------------------------
# TELEMETRY INTEGRATION
# ----------------------------------------

def test_record_telemetry_sets_device_online():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org"
    )

    telemetry = Telemetry(
        device_id=device.id,
        payload={"temperature": 22.5},
        received_at=datetime(2024, 1, 1, 12, 0, 0)
    )

    service.record_telemetry(device, telemetry)

    assert device.is_online is True
    assert device.last_seen == telemetry.received_at
    assert isinstance(device.pull_events()[0], DeviceBecameOnline)


def test_record_telemetry_updates_last_seen():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org"
    )

    t1 = Telemetry(
        device_id=device.id,
        payload={"t": 1},
        received_at=datetime(2024, 1, 1, 12, 0, 0)
    )

    t2 = Telemetry(
        device_id=device.id,
        payload={"t": 2},
        received_at=datetime(2024, 1, 1, 12, 5, 0)
    )

    service.record_telemetry(device, t1)
    service.record_telemetry(device, t2)

    assert device.last_seen == t2.received_at
    assert isinstance(device.pull_events()[0], DeviceBecameOnline)


# ----------------------------------------
# EVENTS
# ----------------------------------------

def test_device_emits_events():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    device.mark_online(datetime(2024, 1, 1, 12, 0, 0))

    events = device.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], DeviceBecameOnline)