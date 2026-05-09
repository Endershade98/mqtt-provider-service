# src/infrastructure/mqtt/client.py

import json
import logging
from typing import Optional

import paho.mqtt.client as mqtt

from src.application.ports.mqtt import MQTTMessageHandlerPort

logger = logging.getLogger(__name__)


class MQTTClient:

    def __init__(
        self,
        broker: str,
        port: int,
        topic: str,
        message_handler: MQTTMessageHandlerPort,
        client_id: Optional[str] = None,
        keepalive: int = 60,
    ):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.keepalive = keepalive
        self.message_handler = message_handler

        self.client = mqtt.Client(
            client_id=client_id,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        self.client.will_set(
            topic="system/lwt",
            payload=json.dumps({"status": "disconnected"}),
            qos=1,
        )

    def start(self):
        self.client.connect(self.broker, self.port, self.keepalive)
        self.client.loop_forever()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(self.topic)

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning("Unexpected disconnect")
            try:
                client.reconnect()
            except Exception:
                logger.exception("Reconnect failed")

    def _on_message(self, client, userdata, msg):
        payload = self._safe_parse(msg.payload)

        if payload is None:
            return

        try:
            self.message_handler.handle(msg.topic, payload)
        except Exception:
            logger.exception("Handler error")

    def _safe_parse(self, raw: bytes):
        try:
            return json.loads(raw.decode())
        except Exception:
            return None