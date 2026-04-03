
import json
import logging
import paho.mqtt.client as mqtt
from src.services.telemetry_service import TelemetryService

logger = logging.getLogger(__name__)


class MQTTClient:
    def __init__(self, broker="localhost", port=1883):
        self.MQTT_BROKER = broker
        self.MQTT_PORT = port

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected with result code {rc}")
        client.subscribe("prod/+/+/+/telemetry")

    def on_message(self, client, userdata, msg):
        logger.info(f"Message received on {msg.topic}")

        try:
            payload = json.loads(msg.payload.decode())

            # delega al service
            telemetry_service = TelemetryService()
            telemetry_service.handle_telemetry(msg.topic, payload)

        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def start_mqtt(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(self.MQTT_BROKER, self.MQTT_PORT, 60)
        client.loop_forever()