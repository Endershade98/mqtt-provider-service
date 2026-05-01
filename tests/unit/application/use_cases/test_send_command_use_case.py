# tests/unit/application/use_cases/test_send_command_use_case.py

from unittest.mock import Mock

from src.application.use_cases.dto.send_command_dto import SendCommandDTO
from src.application.use_cases.send_command import SendCommandUseCase


def test_send_command_use_case_executes_flow():
    repo = Mock()
    outbox = Mock()
    mqtt = Mock()

    uc = SendCommandUseCase(repo, outbox, mqtt)

    dto = SendCommandDTO(
        command_id="cmd1",
        device_id="dev1",
        payload={"action": "reboot"}
    )

    result = uc.execute(dto)

    assert repo.save.called
    assert outbox.save.called
    assert mqtt.publish.called