# tests/integration/interfaces/mqtt/test_translator.py

from datetime import datetime

from src.interfaces.mqtt.translator import MQTTMessageTranslator
from src.application.use_cases.dto.handle_telemetry_dto import HandleTelemetryDTO
from src.application.use_cases.dto.ack_command_dto import AckCommandDTO


def test_translate_telemetry_contract():
    translator = MQTTMessageTranslator()

    now = datetime.utcnow()

    result = translator.translate_telemetry(
        topic="devices/dev1/telemetry",
        payload={"temp": 22},
        received_at=now,
    )

    assert isinstance(result, HandleTelemetryDTO)
    assert result.device_id == "dev1"
    assert result.payload == {"temp": 22}
    assert result.received_at == now


def test_translate_ack_contract():
    translator = MQTTMessageTranslator()

    result = translator.translate_ack(
        topic="devices/dev1/ack",
        payload={"command_id": "cmd1"},
        received_at=datetime.utcnow(),
    )

    assert isinstance(result, AckCommandDTO)
    assert result.command_id == "cmd1"