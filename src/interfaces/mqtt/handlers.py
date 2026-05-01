# src/interfaces/mqtt/handlers.py

from src.interfaces.mqtt.translator import MQTTMessageTranslator
from src.interfaces.mqtt.dispatcher import MQTTDispatcher


class MQTTHandler:

    def __init__(self, translator: MQTTMessageTranslator, dispatcher: MQTTDispatcher):
        self.translator = translator
        self.dispatcher = dispatcher

    def handle(self, topic: str, payload: dict):

        envelope = self.translator.translate(topic, payload)

        return self.dispatcher.dispatch(envelope)