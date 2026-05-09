# tests/integration/application/test_send_command_flow.py

import pytest

from src.application.use_cases.send_command import SendCommandUseCase
from src.application.use_cases.dto.send_command_dto import SendCommandDTO

from src.infrastructure.persistence.django.repositories.command_repository import DjangoCommandRepository
from src.infrastructure.persistence.django.repositories.outbox_repository import DjangoOutboxRepository
from src.infrastructure.persistence.django.unit_of_work import DjangoUnitOfWork


@pytest.mark.django_db
def test_send_command_flow():
    repo = DjangoCommandRepository()
    outbox = DjangoOutboxRepository()
    uow = DjangoUnitOfWork()

    use_case = SendCommandUseCase(repo, uow, outbox)

    dto = SendCommandDTO(
        command_id="cmd-1",
        device_id="dev-1",
        payload={"power": "on"},
    )

    use_case.execute(dto)

    command = repo.get(type("X", (), {"value": "cmd-1"})())

    assert command.status.value == "SENT"