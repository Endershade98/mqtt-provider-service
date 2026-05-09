# tests/integration/interfaces/mqtt/test_topic_parser.py

import pytest

from src.interfaces.mqtt.topic import Topic, TopicChannel
from src.domain.shared.exceptions import InvalidTopicFormat


def test_topic_parsing():
    topic = Topic("devices/dev1/command")

    assert topic.device_id.value == "dev1"
    assert topic.channel == TopicChannel.COMMAND


def test_invalid_topic_raises():
    with pytest.raises(InvalidTopicFormat):
        Topic("invalid/topic")