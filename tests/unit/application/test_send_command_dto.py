# tests/unit/application/test_send_command_dto.py

from src.application.use_cases.dto.send_command_dto import SendCommandDTO


def test_send_command_dto_creation():
    dto = SendCommandDTO(
        command_id="cmd-1",
        device_id="dev-1",
        payload={"action": "reboot"}
    )

    assert dto.command_id == "cmd-1"
    assert dto.device_id == "dev-1"
    assert dto.payload["action"] == "reboot"