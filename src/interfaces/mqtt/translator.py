# src/interfaces/mqtt/translator.py

from datetime import datetime

from src.interfaces.mqtt.topic import Topic
from src.application.use_cases.dto.handle_telemetry_dto import HandleTelemetryDTO
from src.application.use_cases.dto.ack_command_dto import AckCommandDTO


class MQTTMessageTranslator:

    def translate_telemetry(
        self,
        topic: str,
        payload: dict,
        received_at: datetime
    ) -> HandleTelemetryDTO:

        topic_vo = Topic(topic)

        return HandleTelemetryDTO(
            device_id=topic_vo.device_id.value,
            payload=payload,
            received_at=received_at,
        )

    def translate_ack(
        self,
        topic: str,
        payload: dict,
        received_at: datetime
    ) -> AckCommandDTO:

        Topic(topic)  # validation only

        return AckCommandDTO(
            command_id=payload.get("command_id"),
        )