from lib.mqtt_client.subscriber import Subscriber
import logging
from dotenv import load_dotenv
from config.config import MQTT_SUBSCRIBER_CONFIG

# Load environment variables from .env file
load_dotenv('.env')
# Configure Environment Variables
BROKER_ADDRESS = MQTT_SUBSCRIBER_CONFIG["broker_address"]
PORT = MQTT_SUBSCRIBER_CONFIG["port"]
TOPIC = MQTT_SUBSCRIBER_CONFIG["topic"]

# Entry point
if __name__ == "__main__":
    subscriber = Subscriber(broker_address=BROKER_ADDRESS, port=PORT, topic=TOPIC)
    subscriber.run() # Connect and start the subscriber
    