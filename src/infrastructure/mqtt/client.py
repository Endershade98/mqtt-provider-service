# src/infrastructure/mqtt/client.py
import json
import logging
import time
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class MQTTClient:

    def __init__(
        self,
        broker: str,
        port: int,
        topic: str,
        message_handler,   # ← dependency injection
        client_id: str = None,
        keepalive: int = 60,
    ):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.keepalive = keepalive
        self.message_handler = message_handler

        self.client = mqtt.Client(client_id=client_id, clean_session=True)

        # callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        # LWT (Last Will)
        self.client.will_set(
            topic="system/lwt",
            payload=json.dumps({"status": "disconnected"}),
            qos=1,
            retain=False
        )

    # ------------------------
    # CONNECTION HANDLING
    # ------------------------

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT connected successfully")
            client.subscribe(self.topic)
            logger.info(f"Subscribed to topic: {self.topic}")
        else:
            logger.error(f"MQTT connection failed with code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logger.warning(f"MQTT disconnected with code {rc}")

        # auto-reconnect loop
        while True:
            try:
                logger.info("Attempting MQTT reconnection...")
                client.reconnect()
                logger.info("MQTT reconnected successfully")
                break
            except Exception as e:
                logger.error(f"Reconnection failed: {e}")
                time.sleep(5)

    # ------------------------
    # MESSAGE HANDLING
    # ------------------------

    def on_message(self, client, userdata, msg):
        logger.info(f"Message received on topic: {msg.topic}")

        try:
            payload = json.loads(msg.payload.decode())
        except Exception as e:
            logger.error(f"Invalid JSON payload: {e}")
            return

        try:
            # delegate to handler (NO business logic here)
            self.message_handler.handle(msg.topic, payload)
        except Exception as e:
            logger.exception(f"Error in message handler: {e}")

    # ------------------------
    # START LOOP
    # ------------------------

    def start(self):
        logger.info("Starting MQTT client...")

        self.client.connect(self.broker, self.port, self.keepalive)

        # NON blocca il thread principale se usi container dedicato
        self.client.loop_forever()