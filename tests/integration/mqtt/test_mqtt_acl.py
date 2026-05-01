# tests/integration/mqtt/test_mqtt_acl.py

from src.interfaces.mqtt.translator import MQTTMessageTranslator


def test_mqtt_rejects_invalid_topic():

    translator = MQTTMessageTranslator()

    result = translator.translate(
        topic="invalid/topic",
        payload={"action": "reboot"}
    )

    assert result is None


def test_mqtt_rejects_missing_payload_fields():

    translator = MQTTMessageTranslator()

    result = translator.translate(
        topic="devices/device123/command",
        payload={}
    )

    assert result is None


def test_mqtt_accepts_valid_command():

    translator = MQTTMessageTranslator()

    result = translator.translate(
        topic="devices/device123/command",
        payload={
            "command_id": "cmd-1",
            "payload": {"action": "reboot"}
        }
    )

    assert result is not None
    assert result.device_id.value == "device123"