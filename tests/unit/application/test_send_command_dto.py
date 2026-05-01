# tests/unit/application/test_send_command_dto.py

from src.application.use_cases.dto.send_command_dto import SendCommandDTO


def test_send_command_dto_is_immutable():
    dto = SendCommandDTO(
        command_id="cmd1",
        device_id="dev1",
        payload={"action": "reboot"}
    )

    assert dto.command_id == "cmd1"
    assert dto.device_id == "dev1"