# src/application/use_cases/ack_command.py

class AcknowledgeCommandUseCase:

    def __init__(self, command_repository, outbox):
        self.command_repository = command_repository
        self.outbox = outbox

    def execute(self, command):

        command.ack()

        events = command.pull_events()

        self.command_repository.save(command)
        self.outbox.save(events)

        return events