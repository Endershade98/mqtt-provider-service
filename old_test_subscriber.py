import pytest
from unittest.mock import MagicMock, patch
from lib.mqtt_client.subscriber import Subscriber
import paho.mqtt.client as mqtt


def test_subscriber_initialization():
    """Test the initialization of the Subscriber class"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    assert subscriber.broker_address == "test.mosquitto.org"
    assert subscriber.port == 1883
    assert subscriber.topic == "/test/topic"


def test_subscriber_initialization_invalid_broker():
    """Test initialization with an invalid broker address"""
    with pytest.raises(ValueError):
        Subscriber(broker_address="", port=1883, topic="test/topic")


def test_subscriber_initialization_invalid_port():
    """Test initialization with an invalid port number"""
    with pytest.raises(ValueError):
        Subscriber(broker_address="test.mosquitto.org", port=-1, topic="test/topic")


def test_subscriber_initialization_invalid_topic():
    """Test initialization with an invalid topic"""
    with pytest.raises(ValueError):
        Subscriber(broker_address="test.mosquitto.org", port=1883, topic="")


def test_subscriber_connect():
    """Test the connect method of the subscriber class"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    with patch.object(subscriber.client, "connect", return_value=None) as mock_connect:
        subscriber.connect()
        mock_connect.assert_called_once_with("test.mosquitto.org", 1883, keepalive=60)


def test_subscriber_connect_failure():
    """Test the connect method with a failure scenario"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    with patch.object(subscriber.client, "connect", side_effect=Exception("Connection failed")):
        with pytest.raises(ConnectionError):
            subscriber.connect()


def test_subscriber_subscribe():
    """Test the subscribe method of the subscriber class"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    with patch.object(subscriber.client, "subscribe", return_value=None) as mock_subscribe:
        subscriber.subscribe()
        mock_subscribe.assert_called_once_with("/test/topic")


def test_subscriber_subscribe_failure():
    """Test the subscribe method with a failure scenario"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    with patch.object(subscriber.client, "subscribe", side_effect=Exception("Subscription failed")):
        with pytest.raises(ConnectionError):
            subscriber.subscribe()


def test_subscriber_on_connect():
    """Test the on_connect callback"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    mock_client = MagicMock()
    mock_reason_code = MagicMock()
    mock_reason_code.value = 0
    with patch.object(subscriber.client, "subscribe", return_value=None) as mock_subscribe:
        subscriber.on_connect(mock_client, None, {}, mock_reason_code, None)
        mock_subscribe.assert_called_once_with("test/topic")


def test_subscriber_on_disconnect():
    """Test the on_disconnect callback"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    mock_client = MagicMock()
    subscriber.on_disconnect(mock_client, None, 0, None)
    mock_client.loop_stop.assert_called_once()


def test_subscriber_on_message():
    """Test the on_message callback"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    mock_client = MagicMock()
    mock_msg = MagicMock()
    mock_msg.topic = "/test/topic"
    mock_msg.payload = b"Test message"
    with patch.object(subscriber, "process_mqtt_message", return_value=None) as mock_process:
        subscriber.on_message(mock_client, None, mock_msg)
        mock_process.assert_called_once_with("Test message", "/test/topic")


def test_subscriber_run():
    """Test the run method of the subscriber class"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    with patch.object(subscriber.client, "loop_forever", return_value=None) as mock_loop_forever:
        subscriber.run()
        mock_loop_forever.assert_called()


def test_subscriber_stop():
    """Test the stop method of the subscriber class"""
    subscriber = Subscriber(broker_address="test.mosquitto.org", port=1883, topic="test/topic")
    with patch.object(subscriber.client, "unsubscribe", return_value=None) as mock_unsubscribe:
        with patch.object(subscriber.client, "loop_stop", return_value=None) as mock_loop_stop:
            with patch.object(subscriber.client, "is_connected", return_value=False):
                subscriber.stop()
                mock_unsubscribe.assert_called_once_with("/test/topic")
                mock_loop_stop.assert_called_once()
                assert subscriber.client.is_connected() is False
