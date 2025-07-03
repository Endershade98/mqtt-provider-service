from dotenv import load_dotenv
import os

MQTT_SUBSCRIBER_CONFIG = {
    "broker_address": os.getenv("MQTT_BROKER_ADDRESS", "test.mosquitto.org"),
    "port": int(os.getenv("MQTT_PORT", 1883)),
    "topic": os.getenv("MQTT_TOPIC", "test/topic")
}