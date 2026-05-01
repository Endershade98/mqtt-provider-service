# tests/unit/interfaces/test_mqtt_dto.py

from src.interfaces.mqtt.translator import MQTTMessageTranslator


def test_telemetry_dto_is_pure():
    translator = MQTTMessageTranslator()

    dto = translator.translate(
        topic="devices/device123/telemetry",
        payload={"temp": 20}
    )

    assert dto.device_id == "device123"
    assert dto.payload == {"temp": 20}