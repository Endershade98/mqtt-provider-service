# tests/unit/domain/device/test_device.py
import pytest
from datetime import datetime, timedelta
from django.utils import timezone

from src.application.services.device_service import DeviceService
from src.domain.device.entity import Device
from src.domain.device.events import (
    DeviceBecameOnline,
    DeviceBecameOffline,
    DeviceMarkedStale,
)
from src.domain.device.value_objects import DeviceId
from src.domain.telemetry.entity import Telemetry


service = DeviceService()

date = timezone.make_aware(datetime(2024, 1, 1, 12, 0, 0))


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

    device.mark_online(date)

    events = device.pull_events()

    assert device.is_online is True
    assert device.last_seen == date
    assert any(isinstance(e, DeviceBecameOnline) for e in events)


def test_mark_online_idempotent():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456"
    )

    device.mark_online(date)
    device.mark_online(date)  # stesso timestamp

    events = device.pull_events()

    assert device.is_online is True
    assert len([e for e in events if isinstance(e, DeviceBecameOnline)]) == 1


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

    device.mark_online(date)
    device.mark_offline(date)

    events = device.pull_events()

    assert device.is_online is False
    assert any(isinstance(e, DeviceBecameOffline) for e in events)


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

    device.mark_online(date)
    device.pull_events()

    now = date + timedelta(minutes=2)

    device.check_stale(now, threshold_seconds=300)

    assert device.is_online is True
    assert len(device.pull_events()) == 0


def test_device_becomes_stale():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test",
        device_type="sensor",
        organization="org"
    )

    device.mark_online(date)

    now = date + timedelta(minutes=10)

    device.check_stale(now, threshold_seconds=300)

    events = device.pull_events()

    assert device.is_online is False
    assert any(isinstance(e, DeviceMarkedStale) for e in events)


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
        received_at=date
    )

    service.record_telemetry(device, telemetry)

    events = device.pull_events()

    assert device.is_online is True
    assert device.last_seen == telemetry.received_at
    assert any(isinstance(e, DeviceBecameOnline) for e in events)


def test_record_telemetry_updates_last_seen():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org"
    )

    t1 = Telemetry(device_id=device.id, payload={"t": 1}, received_at=date)
    t2 = Telemetry(device_id=device.id, payload={"t": 2}, received_at=date + timedelta(minutes=5))

    service.record_telemetry(device, t1)
    service.record_telemetry(device, t2)

    assert device.last_seen == t2.received_at


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

    device.mark_online(date)

    events = device.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], DeviceBecameOnline)


# ❌ FIXATI: ora coerenti col dominio (NO mark_online() senza now)

def test_device_mark_online_generates_event():
    device = Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org"
    )

    device.mark_online(date)

    events = device.pull_events()

    assert any(isinstance(e, DeviceBecameOnline) for e in events)


def test_device_does_not_duplicate_online_event():
    device = Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org",
        is_online=True
    )

    device.mark_online(date)

    events = device.pull_events()

    assert len([e for e in events if isinstance(e, DeviceBecameOnline)]) <= 1


def test_device_updates_last_seen():
    device = Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org"
    )

    device.mark_online(date)

    assert device.last_seen is not None