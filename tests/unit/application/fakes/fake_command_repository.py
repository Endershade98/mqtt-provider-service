# tests/unit/application/fakes/fake_command_repository.py

class FakeCommandRepository:
    def __init__(self):
        self.commands = {}

    def save(self, command):
        self.commands[command.command_id.value] = command

    def get(self, command_id):
        return self.commands.get(command_id.value)