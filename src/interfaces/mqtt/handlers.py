# src/interfaces/mqtt/handlers.py

from src.interfaces.mqtt.translator import MQTTMessageTranslator
from src.application.use_cases.mqtt_router import MQTTApplicationRouter
from src.interfaces.mqtt.topic import Topic, TopicChannel


class MQTTHandler:

    def __init__(self, translator: MQTTMessageTranslator, router: MQTTApplicationRouter):
        self.translator = translator
        self.router = router

    def handle(self, topic: str, payload: dict, received_at):

        topic_vo = Topic(topic)

        if topic_vo.channel == TopicChannel.TELEMETRY:
            dto = self.translator.translate_telemetry(topic, payload, received_at)
            return self.router.handle_telemetry(dto)

        if topic_vo.channel == TopicChannel.ACK:
            dto = self.translator.translate_ack(topic, payload, received_at)
            return self.router.handle_ack(dto)

        raise ValueError(f"Unsupported topic: {topic}")