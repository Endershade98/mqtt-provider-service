# src/interfaces/mqtt/translator.py
from dataclasses import dataclass
from src.domain.device.value_objects import Topic, DeviceId, TopicChannel


@dataclass
class TelemetryDTO:
    device_id: DeviceId
    payload: dict


@dataclass
class CommandAckDTO:
    device_id: DeviceId
    payload: dict


class MQTTMessageTranslator:

    def translate(self, topic: str, payload: dict):
        topic_vo = Topic(topic)

        channel = topic_vo.get_channel()
        device_id = topic_vo.get_device_id()

        if channel == TopicChannel.TELEMETRY:
            return TelemetryDTO(device_id=device_id.value, payload=payload)

        elif channel == TopicChannel.ACK:
            return CommandAckDTO(device_id=device_id.value, payload=payload)

        else:
            raise ValueError(f"Unsupported channel: {channel}")