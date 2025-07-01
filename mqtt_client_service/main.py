from mqtt_client_service.subscriber import Subscriber
import logging

def main():
    # Create a Subscriber instance with the broker address and topic
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")

    # Connect to the MQTT broker
    subscriber.connect()

    # Subscribe to the specified topic
    subscriber.subscribe()

    # Keep the script running to listen for messages
    subscriber.run()

# Entry point
if __name__ == "__main__":
    main()
else:
    logging.warning("This script is intended to be run as a standalone application. Importing it may not work as expected.")
    