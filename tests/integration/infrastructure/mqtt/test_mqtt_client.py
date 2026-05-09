# tests/integration/infrastructure/mqtt/test_mqtt_client.py

import json
from unittest.mock import Mock, MagicMock

from src.infrastructure.mqtt.client import MQTTClient


class FakeHandler:
    def __init__(self):
        self.calls = []

    def handle(self, topic, payload):
        self.calls.append((topic, payload))


def make_client(handler):
    return MQTTClient(
        broker="localhost",
        port=1883,
        topic="test/topic",
        message_handler=handler,
        client_id="test"
    )


def test_on_message_valid_json_calls_handler():
    handler = FakeHandler()
    client = make_client(handler)

    msg = MagicMock()
    msg.topic = "test/topic"
    msg.payload = json.dumps({"a": 1}).encode()

    client._on_message(None, None, msg)

    assert handler.calls == [("test/topic", {"a": 1})]


def test_on_message_invalid_json_is_ignored():
    handler = FakeHandler()
    client = make_client(handler)

    msg = MagicMock()
    msg.topic = "test/topic"
    msg.payload = b"invalid-json"

    client._on_message(None, None, msg)

    assert handler.calls == []


def test_handler_exception_does_not_crash():
    class BadHandler:
        def handle(self, topic, payload):
            raise Exception("boom")

    client = make_client(BadHandler())

    msg = MagicMock()
    msg.topic = "test/topic"
    msg.payload = json.dumps({"x": 1}).encode()

    # non deve lanciare
    client._on_message(None, None, msg)


def test_safe_parse_returns_none_on_bad_payload():
    handler = FakeHandler()
    client = make_client(handler)

    assert client._safe_parse(b"not-json") is None