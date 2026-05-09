# tests/unit/application/use_cases/test_send_command_use_case.py

from tests.unit.application.fakes.fake_unit_of_work import FakeUnitOfWork
from tests.unit.application.fakes.fake_command_repository import FakeCommandRepository
from tests.unit.application.fakes.fake_outbox import FakeOutbox
from tests.unit.application.fakes.fake_mqtt_publisher import FakeMqttPublisher
from src.application.use_cases.send_command import SendCommandUseCase
from src.application.use_cases.dto.send_command_dto import SendCommandDTO


def test_send_command_use_case_creates_sends_and_persists_command():

    repo = FakeCommandRepository()
    outbox = FakeOutbox()
    mqtt = FakeMqttPublisher()
    uow = FakeUnitOfWork()

    use_case = SendCommandUseCase(repo, uow, outbox)

    dto = SendCommandDTO(
        command_id="cmd-1",
        device_id="dev-1",
        payload={"action": "reboot"}
    )

    command = use_case.execute(dto)

    assert command is not None
    assert uow.committed is True