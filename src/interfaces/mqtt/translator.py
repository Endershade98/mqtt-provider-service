# src/interfaces/mqtt/translator.py

from dataclasses import dataclass
from src.interfaces.mqtt.topic_parser import Topic, TopicChannel


@dataclass(frozen=True)
class MQTTEnvelope:
    device_id: str
    channel: TopicChannel
    payload: dict
    received_at: str | None = None


class MQTTMessageTranslator:

    def translate(self, topic: str, payload: dict) -> MQTTEnvelope:

        topic_vo = Topic(topic)

        return MQTTEnvelope(
            device_id=topic_vo.get_device_id().value,
            channel=topic_vo.get_channel(),
            payload=payload,
        )