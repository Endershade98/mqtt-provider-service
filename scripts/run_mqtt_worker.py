# scripts/run_mqtt_worker.py

import os
import logging

from src.application.use_cases.mqtt_router import MQTTApplicationRouter
from src.infrastructure.mqtt.client import MQTTClient
from src.interfaces.mqtt.handlers import MQTTHandler
from src.interfaces.mqtt.translator import MQTTMessageTranslator

from src.application.use_cases.handle_telemetry import HandleTelemetryUseCase
from src.application.use_cases.ack_command import AcknowledgeCommandUseCase

from src.infrastructure.persistence.django.repositories import (
    DeviceRepositoryImpl,
    CommandRepositoryImpl,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    logger.info("Bootstrapping MQTT worker...")

    device_repo = DeviceRepositoryImpl()
    command_repo = CommandRepositoryImpl()

    telemetry_uc = HandleTelemetryUseCase(
        device_repository=device_repo,
    )

    ack_uc = AcknowledgeCommandUseCase(
        command_repository=command_repo,
    )

    translator = MQTTMessageTranslator()

    router = MQTTApplicationRouter(
        telemetry_uc=telemetry_uc,
        ack_uc=ack_uc,
    )

    handler = MQTTHandler(
        translator=translator,
        router=router,
    )

    client = MQTTClient(
        broker=os.getenv("MQTT_BROKER_HOST", "mqtt"),
        port=int(os.getenv("MQTT_BROKER_PORT", 1883)),
        topic="iot/devices/+/+",
        message_handler=handler,
        client_id="mqtt-worker",
    )

    logger.info("MQTT worker started")
    client.start()


if __name__ == "__main__":
    main()