# tests/unit/application/fakes/fake_command_repository.py

from src.domain.command.value_objects import CommandId


class FakeCommandRepository:
    def __init__(self):
        self.storage = {}

    def save(self, command):
        self.storage[command.command_id.value] = command

    def get(self, command_id: CommandId):
        return self.storage.get(command_id.value)