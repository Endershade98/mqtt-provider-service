# tests/integration/mqtt/test_mqtt_flow.py

def test_real_mqtt_flow(db):
    from unittest.mock import Mock
    from src.interfaces.mqtt.handlers import MQTTHandler
    from src.interfaces.mqtt.translator import MQTTMessageTranslator

    mock_use_case = Mock()

    translator = MQTTMessageTranslator()

    handler = MQTTHandler(
        telemetry_uc=mock_use_case,
        ack_uc=Mock(),
        translator=translator
    )

    topic = "iot/devices/device123/telemetry"
    payload = {"temp": 25}

    handler.handle(topic, payload)

    mock_use_case.execute.assert_called_once()