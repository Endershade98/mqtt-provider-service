# tests/unit/domain/shared/test_value_objects.py

import pytest

from src.domain.device.value_objects import DeviceId
from src.domain.shared.exceptions import InvalidDeviceId


def test_device_id_valid():
    assert DeviceId("dev-1").value == "dev-1"


def test_device_id_invalid():
    with pytest.raises(InvalidDeviceId):
        DeviceId("")