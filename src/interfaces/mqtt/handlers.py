# src/interfaces/mqtt/handlers.py

from src.interfaces.mqtt.translator import MQTTMessageTranslator
from src.application.use_cases.mqtt_router import MQTTApplicationRouter


class MQTTHandler:

    def __init__(self, translator: MQTTMessageTranslator, router: MQTTApplicationRouter):
        self.translator = translator
        self.router = router

    def handle(self, topic: str, payload: dict, received_at):

        if topic.endswith("telemetry"):
            contract = self.translator.translate_telemetry(topic, payload, received_at)
            return self.router.handle_telemetry(contract)

        if topic.endswith("ack"):
            contract = self.translator.translate_ack(topic, payload, received_at)
            return self.router.handle_ack(contract)

        raise ValueError(f"Unsupported topic: {topic}")