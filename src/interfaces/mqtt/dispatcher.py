# src/interfaces/mqtt/dispatcher.py
from typing import Any, Dict, Type


class MQTTDispatcher:
    def __init__(self, routes: Dict[Type, Any]):
        self.routes = routes

    def dispatch(self, dto):
        handler = self.routes.get(type(dto))

        if not handler:
            raise ValueError(f"No handler for DTO type: {type(dto)}")

        return handler.execute(
            device_id=dto.device_id,
            payload=dto.payload
        )