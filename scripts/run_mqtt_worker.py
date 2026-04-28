# scripts/run_mqtt_worker.py
import os

from src.infrastructure.mqtt.client import MQTTClient
from src.interfaces.mqtt.handlers import MQTTHandler
from src.interfaces.mqtt.translator import MQTTMessageTranslator

from src.application.use_cases.handle_telemetry import HandleTelemetryUseCase
from src.infrastructure.persistence.django.repositories import DeviceRepositoryImpl


def main():
    # dependencies
    device_repo = DeviceRepositoryImpl()
    use_case = HandleTelemetryUseCase(device_repo=device_repo)

    translator = MQTTMessageTranslator()

    handler = MQTTHandler(
        telemetry_use_case=use_case,
        translator=translator
    )

    client = MQTTClient(
        broker=os.getenv("MQTT_BROKER", "mqtt"),
        port=int(os.getenv("MQTT_PORT", 1883)),
        topic="devices/+/telemetry",
        message_handler=handler,
        client_id="mqtt-worker"
    )

    client.start()


if __name__ == "__main__":
    main()