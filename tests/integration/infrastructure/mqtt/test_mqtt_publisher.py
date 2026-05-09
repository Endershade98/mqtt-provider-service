# tests/integration/infrastructure/mqtt/test_mqtt_publisher.py

import pytest
from src.infrastructure.mqtt.publisher import MqttPublisher


class TestPublisher(MqttPublisher):

    def __init__(self):
        self.published = []

    def publish(self, topic: str, payload: dict):
        self.published.append((topic, payload))


def test_publish_command_builds_correct_topic_and_payload():
    pub = TestPublisher()

    pub.publish_command(
        command_id="cmd-1",
        device_id="dev-1",
        payload={"x": 1},
        status="SENT"
    )

    assert len(pub.published) == 1

    topic, payload = pub.published[0]

    assert topic == "devices/dev-1/command"
    assert payload == {
        "command_id": "cmd-1",
        "device_id": "dev-1",
        "payload": {"x": 1},
        "status": "SENT",
    }