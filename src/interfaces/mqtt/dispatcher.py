# src/interfaces/mqtt/dispatcher.py

from src.interfaces.mqtt.adapters import MQTTToApplicationAdapter


class MQTTDispatcher:

    def __init__(self, routes):
        self.routes = routes

    def dispatch(self, envelope):

        key, dto = MQTTToApplicationAdapter.resolve(envelope)

        use_case = self.routes.get(key)

        if not use_case:
            raise ValueError(f"No handler for key: {key}")

        return use_case.execute(dto)