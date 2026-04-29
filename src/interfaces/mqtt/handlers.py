# src/interfaces/mqtt/handlers.py
import logging

from src.interfaces.mqtt.translator import TelemetryDTO, CommandAckDTO

logger = logging.getLogger(__name__)


class MQTTHandler:

    def __init__(self, telemetry_uc, ack_uc, translator):
        self.telemetry_uc = telemetry_uc
        self.ack_uc = ack_uc
        self.translator = translator

        self.dispatch_table = {
            "TelemetryDTO": self._handle_telemetry,
            "CommandAckDTO": self._handle_ack,
        }

    def handle(self, topic: str, payload: dict):
        dto = self.translator.translate(topic, payload)

        dto_type = dto.__class__.__name__

        handler = self.dispatch_table.get(dto_type)

        if handler is None:
            raise ValueError(f"Unsupported DTO: {dto_type}")

        handler(dto)

    def _handle_telemetry(self, dto):
        self.telemetry_uc.execute(
            device_id=dto.device_id,
            payload=dto.payload
        )

    def _handle_ack(self, dto):
        self.ack_uc.execute(
            device_id=dto.device_id,
            payload=dto.payload
        )