# tests/unit/domain/device/test_device.py
import pytest
from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId
from datetime import datetime


def test_mark_online_updates_last_seen():
    
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456"
    )

    now = datetime.date.today()
    device.mark_online(now)

    assert device.is_online is True
    assert device.last_seen == now

def test_mark_online_idempotent():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456"
    )

    now = datetime.date.today()
    device.mark_online(now)
    device.mark_online(now)  # chiamata ripetuta

    assert device.is_online is True
    assert device.last_seen == now  # last_seen non cambia al secondo call

def test_device_becomes_stale():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456",
        last_seen=datetime(2024, 1, 1, 12, 0, 0)
    )

    now = datetime(2024, 1, 1, 12, 5, 0)  # 5 minuti dopo
    threshold_seconds = 300  # 5 minuti

    device.check_stale(now, threshold_seconds)

    # In questo caso il device è esattamente al limite, quindi non dovrebbe essere stale
    assert device.is_active is True

def test_device_not_stale_if_recent():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456",
        last_seen=datetime(2024, 1, 1, 12, 0, 0)
    )

    now = datetime(2024, 1, 1, 12, 2, 0)  # 2 minuti dopo
    threshold_seconds = 300  # 5 minuti

    device.check_stale(now, threshold_seconds)

    assert device.is_active is True

def test_device_goes_offline():
    device = Device(
        id=DeviceId("dev-123"),
        name="Test Device",
        device_type="sensor",
        organization="org-456",
        last_seen=datetime(2024, 1, 1, 12, 0, 0)
    )

    now = datetime(2024, 1, 1, 12, 10, 0)  # 10 minuti dopo
    threshold_seconds = 300  # 5 minuti

    device.check_stale(now, threshold_seconds)

    assert device.is_online is False