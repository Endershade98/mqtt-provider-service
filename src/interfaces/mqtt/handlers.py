# src/interfaces/mqtt/handlers.py
import logging

from src.interfaces.mqtt.topic_parser import TopicParser
from src.interfaces.mqtt.message import MQTTMessage

logger = logging.getLogger(__name__)

class MQTTHandler:

    def __init__(self, telemetry_uc, ack_uc, translator):
        self.telemetry_uc = telemetry_uc
        self.ack_uc = ack_uc
        self.translator = translator

    def handle(self, topic: str, payload: dict):
        dto = self.translator.translate(topic, payload)

        if hasattr(dto, "payload") and hasattr(dto, "device_id"):
            if dto.__class__.__name__ == "TelemetryDTO":
                self.telemetry_uc.execute(
                    device_id=dto.device_id,
                    payload=dto.payload
                )

            elif dto.__class__.__name__ == "CommandAckDTO":
                self.ack_uc.execute(
                    device_id=dto.device_id,
                    payload=dto.payload
                )