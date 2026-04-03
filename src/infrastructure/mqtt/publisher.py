import json
import paho.mqtt.client as mqtt


class MQTTPublisher:
    def __init__(self, broker="localhost", port=1883):
        self.client = mqtt.Client()
        self.client.connect(broker, port, 60)

    def publish(self, topic: str, payload: dict):
        result = self.client.publish(topic, json.dumps(payload))

        # result.rc == 0 → successo
        if result.rc != 0:
            raise Exception(f"MQTT publish failed with code {result.rc}")