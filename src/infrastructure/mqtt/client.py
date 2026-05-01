# src/infrastructure/mqtt/client.py

import json
import logging
from typing import Optional

import paho.mqtt.client as mqtt

from src.interfaces.mqtt.message import MQTTMessage

logger = logging.getLogger(__name__)


class MQTTClient:
    """
    Infrastructure-level MQTT client.

    Responsibilities:
    - Manage connection lifecycle
    - Handle reconnection
    - Receive raw MQTT messages
    - Convert them into MQTTMessage DTO
    - Delegate handling to the injected handler

    IMPORTANT:
    - No business logic
    - No domain knowledge
    - No repository usage
    """

    def __init__(
        self,
        broker: str,
        port: int,
        topic: str,
        message_handler,
        client_id: Optional[str] = None,
        keepalive: int = 60,
    ):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.keepalive = keepalive
        self.message_handler = message_handler

        self.client = mqtt.Client(client_id=client_id, clean_session=True)

        # Bind callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        # Last Will and Testament (LWT)
        self.client.will_set(
            topic="system/lwt",
            payload=json.dumps({"status": "disconnected"}),
            qos=1,
            retain=False,
        )

    # ==========================================
    # CONNECTION MANAGEMENT
    # ==========================================

    def start(self):
        logger.info("Starting MQTT client...")

        try:
            self.client.connect(self.broker, self.port, self.keepalive)
        except Exception as e:
            logger.exception(f"MQTT connection failed: {e}")
            raise

        # Blocking loop (correct for dedicated container)
        self.client.loop_forever()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("MQTT connected successfully")

            try:
                client.subscribe(self.topic)
                logger.info(f"Subscribed to topic: {self.topic}")
            except Exception as e:
                logger.exception(f"Subscription failed: {e}")

        else:
            logger.error(f"MQTT connection failed with code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        logger.warning(f"MQTT disconnected with code {rc}")

        # Single reconnect attempt (no infinite loop)
        try:
            client.reconnect()
            logger.info("MQTT reconnected successfully")
        except Exception as e:
            logger.error(f"Reconnect failed: {e}")

    # ==========================================
    # MESSAGE HANDLING
    # ==========================================

    def _on_message(self, client, userdata, msg):
        logger.debug(f"Message received on topic: {msg.topic}")

        payload = self._safe_parse_payload(msg.payload)

        if payload is None:
            return

        message = MQTTMessage(
            topic=msg.topic,
            payload=payload,
        )

        try:
            self.message_handler.handle(message.topic, message.payload)
        except Exception:
            logger.exception("Error while handling MQTT message")

    # ==========================================
    # INTERNAL HELPERS
    # ==========================================

    def _safe_parse_payload(self, raw_payload: bytes) -> Optional[dict]:
        try:
            return json.loads(raw_payload.decode())
        except Exception as e:
            logger.error(f"Invalid JSON payload: {e}")
            return None