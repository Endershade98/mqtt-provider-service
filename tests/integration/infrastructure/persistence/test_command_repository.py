# tests/integration/infrastructure/persistence/test_command_repository.py

import pytest

from src.domain.command.entity import Command
from src.domain.command.value_objects import CommandId
from src.domain.device.value_objects import DeviceId
from src.infrastructure.persistence.django.repositories.command_repository import DjangoCommandRepository


@pytest.mark.django_db
def test_command_repository_roundtrip():

    repo = DjangoCommandRepository()

    command = Command.create(
        command_id=CommandId("cmd-1"),
        device_id=DeviceId("dev-1"),
        payload={"action": "reboot"}
    )

    repo.save(command)

    loaded = repo.get(CommandId("cmd-1"))

    assert loaded.command_id.value == "cmd-1"
    assert loaded.payload["action"] == "reboot"