import paho.mqtt.client as mqtt
from mqtt_client_service.utils import log_func_calls
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')

class Subscriber:
    """MQTT Subscriber class to handle incoming messages from a broker"""
    def __init__(self, broker_address: str, topic: str, port: int=1883) -> None:
        if not isinstance(broker_address, str) or not broker_address:
            raise ValueError("Broker address must be a non-empty string")
        else:
            logging.info(f"Broker address {broker_address} is valid")
            self.broker_address = broker_address

        if not isinstance(port, int) or port <= 0:
            raise ValueError("Port must be a positive integer")
        else:
            logging.info(f"Port {port} is valid")
            self.port = port

        if not isinstance(topic, str) or not topic:
            raise ValueError("Topic must be a non-empty string")
        else:
            logging.info(f"Topic {topic} is valid")
            if not topic.startswith('/'):
                topic = '/' + topic
                logging.info(f"Topic normalized to {topic}")
            if topic.endswith('/'):
                topic = topic[:-1]
                logging.info(f"Topic normalized to {topic} (removed trailing '/')")
            self.topic = topic
        
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            protocol=mqtt.MQTTv5,
            client_id="mqtt_energy_client"
        )

        if not isinstance(self.client, mqtt.Client) or not self.client:
            raise ValueError("Failed to create MQTT client instance")
        else:
            logging.info(f"MQTT client instance created successfully for broker {self.broker_address}")

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscribe
        #self.client.on_log = self.on_log

    def connect(self):
        """Connect to the MQTT broker"""
        try:
            self.client.connect(self.broker_address, self.port, keepalive=60)
            logging.info(f"Connected to broker {self.broker_address} on port {self.port}")
        except Exception as e:
            logging.error(f"Failed to connect to broker {self.broker_address}: {e}")
            raise ConnectionError(f"Could not connect to broker {self.broker_address}")
        finally:
            self.client.loop_start()
            logging.info(f"MQTT client loop started for broker {self.broker_address}")

    def disconnect(self):
        """Disconnect from the MQTT broker"""
        try:
            self.client.disconnect()
            logging.info(f"Disconnected from broker {self.broker_address}")
        except Exception as e:
            logging.error(f"Failed to disconnect from broker {self.broker_address}: {e}")
            raise ConnectionError(f"Could not disconnect from broker {self.broker_address}")
        finally:
            self.client.loop_stop()
            logging.info(f"MQTT client loop stopped for broker {self.broker_address}")

    def subscribe(self):
        """Subscribe to the specified topic"""
        try:
            self.client.subscribe(self.topic)
            logging.info(f"Subscribed to topic {self.topic}")
        except Exception as e:
            logging.error(f"Failed to subscribe to topic {self.topic}: {e}")
            raise ConnectionError(f"Could not subscribe to topic {self.topic}")

    def unsubscribe(self):
        """Unsubscribe from the specified topic"""
        try:
            self.client.unsubscribe(self.topic)
            logging.info(f"Unsubscribed from topic {self.topic}")
        except Exception as e:
            logging.error(f"Failed to unsubscribe from topic {self.topic}: {e}")
            raise ConnectionError(f"Could not unsubscribe from topic {self.topic}")

    @log_func_calls
    def on_subscribe(self, client, userdata, mid, reason_code_list, properties, *args, **kwargs):
        """Callback function to handle subscription confirmation"""
        if reason_code_list[0].is_failure:
            logging.error(f"Failed to subscribe to topic '{self.topic}'")
        else:
            logging.info(f"Subscribed to topic '{self.topic}' with QoS {reason_code_list[0].value}")

    @log_func_calls
    def on_unsubscribe(self, client, userdata, mid, reason_code_list, properties, *args, **kwargs):
        """Callback function to handle unsubscription confirmation"""
        if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
            logging.info("unsubscribe succeeded (if SUBACK is received in MQTT it success)")
        else:
            logging.error(f"Broker replied with failure: {reason_code_list[0]}")

    @log_func_calls
    def on_message(self, client, userdata, message, *args, **kwargs):
        """Callback function to handle incoming message"""
        logging.info(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")
        # TODO: Complete this method adding code to process the message

    @log_func_calls
    def on_connect(self, client, userdata, flags, reason_code, properties, *args, **kwargs):
        """Callback function to handle connection to the broker"""
        if reason_code.value == 0:
            logging.info(f"Connected to broker {self.broker_address} with reason code {reason_code}")
            client.subscribe(self.topic)
        else:
            logging.error(f"Failed to connect to broker {self.broker_address} with reason code {reason_code}")

    @log_func_calls
    def on_disconnect(self, client, userdata, reason_code, properties, *args, **kwargs):
        """Callback function to handle disconnection from the broker"""
        logging.info(f"Disconnected from broker {self.broker_address} with reason code: {reason_code}")

    def start(self):
        """Start the subscriber to listen for messages"""
        self.client.subscribe(self.topic)
        logging.info(f"Subscriber started for topic {self.topic} on broker {self.broker_address}")

    def stop(self):
        """Stop the subscriber and disconnect from the broker"""
        if not self.client.is_connected():
            logging.warning(f"Subscriber is not connected to broker {self.broker_address}")
        self.client.unsubscribe(self.topic)
        self.client.loop_stop()
        logging.info(f"Subscriber stopped for topic {self.topic} on broker {self.broker_address}")

    def run(self):
        """Run the subscriber to listen for messages"""
        logging.info(f"Running subscriber for topic {self.topic} on broker {self.broker_address}")
        self.connect()
        self.subscribe()
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            logging.info("Subscriber stopped by user")
            self.stop()
        finally:
            self.client.loop_stop()

    def __str__(self):
        return f"Subscriber(broker_address={self.broker_address}, topic={self.topic})"

    def __repr__(self):
        return self.__str__()
