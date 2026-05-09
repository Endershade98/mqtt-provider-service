# src/interfaces/mqtt/translator.py

from datetime import datetime

from src.interfaces.mqtt.topic import Topic
from src.application.use_cases.dto.mqtt_contracts import (
    TelemetryContract,
    AckContract,
)


class MQTTMessageTranslator:

    def translate_telemetry(self, topic: str, payload: dict, received_at: datetime) -> TelemetryContract:
        topic_vo = Topic(topic)

        return TelemetryContract(
            device_id=topic_vo.device_id.value,
            payload=payload,
            received_at=received_at,
        )

    def translate_ack(self, topic: str, payload: dict, received_at: datetime) -> AckContract:
        Topic(topic)

        return AckContract(
            command_id=payload.get("command_id"),
        )