# tests/integration/db/test_command_repository.py

import pytest

from src.domain.command.entity import Command

from src.domain.device.value_objects import DeviceId
from src.domain.command.value_objects import CommandId

from src.infrastructure.persistence.django.models import CommandModel
from src.infrastructure.persistence.django.repositories.command_repository import DjangoCommandRepository


@pytest.mark.django_db
def test_command_repository_roundtrip():

    repo = DjangoCommandRepository()

    cmd = Command.create(
        command_id=CommandId("cmd-1"),
        device_id=DeviceId("dev-1"),
        payload={"action": "restart"}
    )

    repo.save(cmd)

    loaded = repo.get(CommandId("cmd-1"))

    assert loaded.command_id.value == "cmd-1"
    assert loaded.payload == {"action": "restart"}

def test_command_repository_update_status():

    repo = DjangoCommandRepository()

    cmd = Command.create(
        command_id=CommandId("cmd-2"),
        device_id=DeviceId("dev-2"),
        payload={"action": "update_firmware"}
    )

    repo.save(cmd)

    # Simula l'esecuzione del comando
    cmd.status = "executed"
    repo.save(cmd)

    loaded = repo.get(CommandId("cmd-2"))

    assert loaded.status == "executed"

def test_command_repository_nonexistent():

    repo = DjangoCommandRepository()

    with pytest.raises(CommandModel.DoesNotExist):
        repo.get(CommandId("nonexistent"))

def test_command_repository_idempotent_save():

    repo = DjangoCommandRepository()

    cmd = Command.create(
        command_id=CommandId("cmd-3"),
        device_id=DeviceId("dev-3"),
        payload={"action": "shutdown"}
    )

    repo.save(cmd)
    repo.save(cmd)  # salva di nuovo lo stesso comando

    # Dovrebbe esserci solo un record nel database
    assert CommandModel.objects.filter(id="cmd-3").count() == 1

def test_command_repository_update_nonexistent():

    repo = DjangoCommandRepository()

    cmd = Command.create(
        command_id=CommandId("cmd-4"),
        device_id=DeviceId("dev-4"),
        payload={"action": "restart"}
    )

    # Prova ad aggiornare un comando che non esiste ancora
    cmd.status = "executed"
    repo.save(cmd)  # Dovrebbe creare il comando invece di fallire

    loaded = repo.get(CommandId("cmd-4"))

    assert loaded.status == "executed"