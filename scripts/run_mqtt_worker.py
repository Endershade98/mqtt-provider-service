# scripts/run_mqtt_worker.py
from src.infrastructure.mqtt.client import MQTTClient
from src.interfaces.mqtt.handlers import MQTTHandler
from src.application.telemetry.handle_telemetry import HandleTelemetryUseCase

# TODO: inject repository reale
telemetry_use_case = HandleTelemetryUseCase(device_repository=None)

handler = MQTTHandler(telemetry_use_case)

client = MQTTClient(
    broker="mqtt-broker",
    port=1883,
    topic="prod/+/+/+/telemetry",
    message_handler=handler,
)

client.start()