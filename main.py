from publisher import Publisher
from subscriber import Subscriber

def main():
    broker = "mqtt.eclipse.org"  # Example broker address
    topic = "test/topic"
    publisher = Publisher(broker, topic)
    subscriber = Subscriber(broker, topic)

    # Publish a message
    publisher.publish("Hello MQTT!")
    
    # Keep the script running to listen for messages
    try:
        while True:
            pass
    except KeyboardInterrupt:
        publisher.disconnect()
        subscriber.client.loop_stop()
        print("Disconnected from broker.")

# Main Entry Point for the MQTT publisher and subscriber.
if __name__ == "__main__":
    main()