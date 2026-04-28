# tests/unit/interfaces/test_mqtt_handler.py
from unittest.mock import Mock
from src.interfaces.mqtt.handlers import MQTTHandler


def test_handler_routes_to_use_case():
    mock_telemetry_uc = Mock()
    mock_ack_uc = Mock()
    mock_translator = Mock()

    dto = Mock()
    dto.device_id = "device123"
    dto.payload = {"temp": 25}
    dto.__class__.__name__ = "TelemetryDTO"

    mock_translator.translate.return_value = dto

    handler = MQTTHandler(
        telemetry_uc=mock_telemetry_uc,
        ack_uc=mock_ack_uc,
        translator=mock_translator
    )

    topic = "iot/devices/device123/telemetry"
    payload = {"temp": 25}

    handler.handle(topic, payload)

    mock_telemetry_uc.execute.assert_called_once()