# src/application/ports/mqtt.py

from abc import ABC, abstractmethod


class MQTTMessageHandlerPort(ABC):

    @abstractmethod
    def handle(self, topic: str, payload: dict) -> None:
        """Handle an incoming MQTT message."""
        pass