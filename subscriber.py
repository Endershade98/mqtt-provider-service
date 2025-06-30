from paho.mqtt import Client
from utils import log_func_calls
import logging


class Subscriber:
    """MQTT Subscriber class to handle incoming messages from a broker"""
    def __init__(self, broker_address, topic):
        self.broker_address = broker_address
        self.topic = topic
        self.client = Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.connect(self.broker_address)
        self.client.loop_start()
    
    @log_func_calls
    def on_message(self, client, userdata, message):
        """Callback function to handle incoming message"""
        logging.info(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")
        # Here you can add code to process the message
    
    @log_func_calls
    def on_connect(self, client, username, flags, rc):
        """Callback function to handle connection to the broker"""
        logging.info(f"Connected to broker {self.broker_address} with result code {rc}")
        client.subscribe(self.topic)


