# tests/integration/interfaces/mqtt/test_handler.py

from datetime import datetime

from src.interfaces.mqtt.handlers import MQTTHandler


class FakeTranslator:
    def translate_telemetry(self, topic, payload, received_at):
        return "telemetry_dto"

    def translate_ack(self, topic, payload, received_at):
        return "ack_dto"


class FakeRouter:
    def handle_telemetry(self, dto):
        return f"telemetry:{dto}"

    def handle_ack(self, dto):
        return f"ack:{dto}"


def test_handler_pipeline_telemetry():
    handler = MQTTHandler(
        translator=FakeTranslator(),
        router=FakeRouter(),
    )

    result = handler.handle(
        topic="devices/dev1/telemetry",
        payload={"x": 1},
        received_at=datetime.utcnow(),
    )

    assert result == "telemetry:telemetry_dto"


def test_handler_pipeline_ack():
    handler = MQTTHandler(
        translator=FakeTranslator(),
        router=FakeRouter(),
    )

    result = handler.handle(
        topic="devices/dev1/ack",
        payload={"command_id": "c1"},
        received_at=datetime.utcnow(),
    )

    assert result == "ack:ack_dto"