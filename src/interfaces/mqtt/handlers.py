# src/interfaces/mqtt/handlers.py
import logging
from datetime import datetime
from src.application.use_cases.handle_telemetry import HandleTelemetryInput

logger = logging.getLogger(__name__)


class MQTTHandler:

    def __init__(self, telemetry_uc, ack_uc, translator):
        self.telemetry_uc = telemetry_uc
        self.ack_uc = ack_uc
        self.translator = translator

    def handle(self, topic: str, payload: dict):
        dto = self.translator.translate(topic, payload)

        # POLYMORPHIC DISPATCH (DDD CLEAN)
        dto.handle(self)

    # ======================================
    # HANDLERS (pure application routing)
    # ======================================
    def handle_telemetry(self, dto):
        input_dto = HandleTelemetryInput(
            device_id=dto.device_id,
            payload=dto.payload,
            received_at=datetime.utcnow()
        )

        self.telemetry_uc.execute(input_dto)

    def handle_ack(self, dto):
        self.ack_uc.execute(
            device_id=dto.device_id,
            payload=dto.payload
        )