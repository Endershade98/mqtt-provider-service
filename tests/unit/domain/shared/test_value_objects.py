# tests/unit/domain/shared/test_value_objects.py

import pytest

from src.interfaces.mqtt.topic_parser import Topic

from src.domain.device.value_objects import DeviceId
from src.domain.shared.exceptions import (
    InvalidDeviceId,
    InvalidTopicFormat
)


def test_device_id_valid():
    assert DeviceId("dev-1").value == "dev-1"


def test_device_id_invalid():
    with pytest.raises(InvalidDeviceId):
        DeviceId("")


def test_topic_extract_device_id():
    topic = Topic("devices/org/device123/telemetry")

    assert topic.get_device_id().value == "device123"


def test_topic_invalid_format():
    with pytest.raises(InvalidTopicFormat):
        Topic("broken/topic")