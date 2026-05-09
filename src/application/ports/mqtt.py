# src/application/ports/mqtt.py

from abc import ABC, abstractmethod


class MQTTMessageHandlerPort(ABC):

    @abstractmethod
    def handle(self, topic: str, payload: dict, received_at=None):
        pass