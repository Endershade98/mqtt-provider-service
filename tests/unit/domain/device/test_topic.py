# tests/unit/domain/device/test_topic.py

import pytest

from src.interfaces.mqtt.topic_parser import Topic
from src.domain.shared.exceptions import InvalidTopicFormat


def test_topic_extract_device_id():
    topic = Topic("devices/org/device123/telemetry")

    assert topic.get_device_id().value == "device123"


def test_topic_invalid_format():
    with pytest.raises(InvalidTopicFormat):
        Topic("broken/topic").get_device_id()