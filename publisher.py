from paho.mqtt import Client as MQTTClient
from utils import log_func_calls
import logging
from dotenv import load_dotenv

# load_dotenv() load environment variables from .env file
load_dotenv('.env')
# Constants for MQTT configuration
PUB_MQTT_PORT = 1883
PUB_MQTT_HOST = "mqtt.eclipse.org"
PUB_MQTT_TOPIC = "test/TOPIC"

class Publisher:
    """
    MQTT Publisher class to send messages to a broker
    """
    def __init__(self, broker_address=PUB_MQTT_HOST, topic=PUB_MQTT_TOPIC):
        self.broker_address = broker_address
        self.topic = topic 
        self.client = MQTTClient()
        self.client.on_connect = self.on_connect

        self.client.connect(self.broker_address)
        self.client.loop_start()

    @log_func_calls
    def on_connect(self, client, userdata, flags, rc):
        """Callback function to handle connection to the broker"""
        logging.info(f"Connected to broker {self.broker_address} with result code {rc}")
        client.subscribe(self.topic)
        client.on_message = self.on_message

    @log_func_calls
    async def publish(self, message, qos=0):
        """Publish a message to the specified topic"""
        result = self.client.publish(self.topic, message, qos=qos)
        if result.rc == 0:
            logging.info(f"Message '{message}' sent to topic '{self.topic}")
        else:
            logging.error(f"Failed to send message '{message}' to topic '{self.topic}': {result.rc}")
        return result
    
    @log_func_calls
    def disconnect(self):
        """Diconnect from the broker"""
        self.client.disconnect()
        logging.info(f"Disconnected from broker {self.broker_address}")
    
    def __str__(self):
        return f"Publisher(broker_address={self.broker_address}, topic={self.topic})"
    
    def __repr__(self):
        return f"Publisher(broker_address={self.broker_address}, topic={self.topic})"