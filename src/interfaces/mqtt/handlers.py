# src/interfaces/mqtt/handlers.py
import logging

logger = logging.getLogger(__name__)


class MQTTHandler:

    def __init__(self, telemetry_use_case):
        self.telemetry_use_case = telemetry_use_case

    def handle(self, topic: str, payload: dict):
        logger.info(f"Handling MQTT message: {topic}")

        device_id = self._extract_device_id(topic)

        self.telemetry_use_case.execute(
            device_id=device_id,
            payload=payload
        )

    def _extract_device_id(self, topic: str) -> str:
        parts = topic.split("/")
        return parts[3]  # adattare al tuo schema