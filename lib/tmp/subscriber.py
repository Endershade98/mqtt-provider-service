import paho.mqtt.client as mqtt
import logging
from dotenv import load_dotenv

load_dotenv('.env')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

class Subscriber:
    """MQTT Subscriber class to handle incoming messages from a broker"""
    def __init__(self, broker_address: str, port: int = 1883, topic: str = "") -> None:
        if not isinstance(broker_address, str) or not broker_address:
            raise ValueError("Broker address must be a non-empty string")
        self.broker_address = broker_address

        if not isinstance(port, int) or not (0 < port < 65536):
            raise ValueError("Port must be an integer between 1 and 65535")
        self.port = port

        if not isinstance(topic, str) or not topic:
            raise ValueError("Topic must be a non-empty string")
        if not topic.startswith('/'):
            topic = '/' + topic
        if topic.endswith('/'):
            topic = topic[:-1]
        self.topic = topic

        self.client = mqtt.Client(protocol=mqtt.MQTTv5, client_id="mqtt_energy_client")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscribe
        self.client.on_log = self.on_log

    def connect(self):
        try:
            self.client.connect(self.broker_address, self.port, keepalive=60)
            logger.info(f"Connected to broker {self.broker_address}")
        except Exception as e:
            logger.error(f"Failed to connect to broker {self.broker_address}: {e}")
            raise ConnectionError(f"Could not connect to broker {self.broker_address}")
        finally:
            self.client.loop_start()
            logger.info("MQTT client loop started")

    def disconnect(self):
        try:
            self.client.disconnect()
            logger.info("Disconnected from broker")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
            raise ConnectionError("Could not disconnect")
        finally:
            self.client.loop_stop()
            logger.info("MQTT client loop stopped")

    def subscribe(self):
        try:
            self.client.subscribe(self.topic)
            logger.info(f"Subscribed to topic {self.topic}")
        except Exception as e:
            logger.error(f"Subscription failed: {e}")
            raise ConnectionError("Could not subscribe")

    def unsubscribe(self):
        try:
            self.client.unsubscribe(self.topic)
            logger.info(f"Unsubscribed from topic {self.topic}")
        except Exception as e:
            logger.error(f"Unsubscription failed: {e}")
            raise ConnectionError("Could not unsubscribe")

    def on_connect(self, client, userdata, flags, reason_code, properties=None, *args, **kwargs):
        if getattr(reason_code, "value", None) == 0:
            logger.info("on_connect: Connected successfully")
            client.subscribe(self.topic)
        else:
            logger.error(f"on_connect: Connection failed with code {reason_code}")

    def on_disconnect(self, client, userdata, reason_code, properties=None, *args, **kwargs):
        logger.info("on_disconnect: Disconnected")
        client.loop_stop()

    def on_subscribe(self, client, userdata, mid, reason_codes, properties=None):
        logger.info(f"on_subscribe: Subscribed with reason codes {reason_codes}")

    def on_unsubscribe(self, client, userdata, mid, reason_codes, properties=None):
        logger.info("on_unsubscribe: Unsubscribed")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        logger.info(f"on_message: Message received on {msg.topic}: {payload}")
        self.process_mqtt_message(payload, msg.topic)

    def on_log(self, client, userdata, level, buf):
        logger.debug(f"MQTT log: {buf}")

    def process_mqtt_message(self, message: str, topic: str):
        """Placeholder for processing incoming MQTT messages."""
        logger.info(f"process_mqtt_message: doing something with '{message}' on '{topic}'")

    def run(self):
        self.connect()
        self.subscribe()
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            logger.info("run: Stopped by user")
            self.stop()
        finally:
            self.client.loop_stop()

    def stop(self):
        if not self.client.is_connected():
            logger.warning("stop: client is not connected")
        self.client.unsubscribe(self.topic)
        self.client.loop_stop()
        logger.info("stop: Client stopped")
