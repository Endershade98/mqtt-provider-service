# validation functions for MQTT messages, topics, brokers, ports, Qos levels and client instances

def validate_mqtt_message(message: str) -> bool:
    """Validate MQTT message format"""
    if not isinstance(message, str):
        raise ValueError("Message must be a string")
    if len(message) == 0:
        raise ValueError("Message cannot be empty")
    return True

def validate_mqtt_topic(topic: str) -> bool:
    """Validate MQTT topic format"""
    if not isinstance(topic, str):
        raise ValueError("Topic must be a string")
    if len(topic) == 0:
        raise ValueError("Topic cannot be empty")
    if '/' in topic and topic.startswith('/'):
        raise ValueError("Topic cannot start with '/'")
    return True

def validate_mqtt_broker(broker: str) -> bool:
    """Validate MQTT Broker address format"""
    if not isinstance(broker, str):
        raise ValueError("Broker must be a string")
    if len(broker) == 0:
        raise ValueError("Broker cannot be empty")
    if '/' in broker and broker.startswith('/'):
        raise ValueError("Broker cannot start with '/'")
    return True

def validate_mqtt_port(port: int) -> bool:
    """Validate MQTT port number"""
    if not isinstance(port, int):
        raise ValuError("Port must be an integer")
    if port < 1 or port > 65535:
        raise ValueError("Port must be between 1 and 65535")
    return True

def validate_mqtt_qos(qos: int) -> bool:
    """Validate MQTT QoS level"""
    if not isinstance(qos, int):
        raise Valueerror("Qos must be an integer")
    if qos < 0 or qos > 2:
        raise ValueError("QoS must be 0,1 or 2")
    return True

def validate_mqtt_connection(broker: str, port: int) -> bool:
    """Validate MQTT connection parameters"""
    validate_mqtt_broker(broker)
    validate_mqtt_port(port)
    return True

def validate_mqtt_client(client) -> bool:
    """Valodate MQTT client instance"""
    if not hasattr(client, 'connect'):
        raise ValueError("Client must have a connect method")
    if not hasattr(client, 'publish'):
        raise ValueError("Client must have a publish method")
    if not hasattr(client, 'subscribe'):
        raise ValueError("Client must have a subscribe method")
    return True

