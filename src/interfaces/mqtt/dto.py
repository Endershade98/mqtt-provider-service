# src/interfaces/mqtt/dto.py
from typing import Protocol, Any


class MQTTDTO(Protocol):
    def handle(self, handler: Any) -> None:
        """
        Method to be implemented by all DTOs for handling logic.
        The handler will be the MQTTHandler which will call the appropriate use case.
        """
        pass