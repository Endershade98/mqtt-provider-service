# tests/unit/interfaces/test_mqtt_translator.py

from src.domain.device.value_objects import DeviceId
from src.interfaces.mqtt.translator import MQTTMessageTranslator


def test_translate_telemetry_message():

    topic = "iot/devices/device123/telemetry"
    payload = {"temp": 25}

    translator = MQTTMessageTranslator()
    dto = translator.translate(topic, payload)

    assert dto.device_id == DeviceId("device123")
    assert dto.payload == {"temp": 25}