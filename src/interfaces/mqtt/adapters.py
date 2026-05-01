# src/interfaces/mqtt/adapters.py

from src.application.use_cases.handle_telemetry import HandleTelemetryDTO
from src.application.use_cases.ack_command import AckCommandDTO
from src.interfaces.mqtt.topic_parser import TopicChannel


class MQTTToApplicationAdapter:

    @staticmethod
    def to_telemetry(envelope):
        return HandleTelemetryDTO(
            device_id=envelope.device_id,
            payload=envelope.payload,
        )

    @staticmethod
    def to_ack(envelope):
        return AckCommandDTO(
            device_id=envelope.device_id,
            payload=envelope.payload,
        )

    @staticmethod
    def resolve(envelope):

        if envelope.channel == TopicChannel.TELEMETRY:
            return "telemetry", MQTTToApplicationAdapter.to_telemetry(envelope)

        if envelope.channel == TopicChannel.ACK:
            return "ack", MQTTToApplicationAdapter.to_ack(envelope)

        raise ValueError(f"Unsupported channel {envelope.channel}")