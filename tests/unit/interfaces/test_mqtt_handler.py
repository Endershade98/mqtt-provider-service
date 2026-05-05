# tests/unit/interfaces/test_mqtt_handler.py

from unittest.mock import Mock
from src.interfaces.mqtt.handlers import MQTTHandler


def test_handler_routes_to_use_case():

    mock_device_service = Mock()
    mock_translator = Mock()

    dto = Mock()
    dto.device_id = "device123"
    dto.payload = {"temp": 25}
    dto.__class__.__name__ = "TelemetryDTO"

    mock_translator.translate.return_value = dto

    handler = MQTTHandler(
        device_service=mock_device_service,
        translator=mock_translator
    )

    handler.handle("iot/devices/device123/telemetry", {"temp": 25})

    mock_device_service.record_telemetry.assert_called_once()