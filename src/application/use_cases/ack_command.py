# src/application/use_cases/ack_command.py

from src.application.use_cases.base import UseCase
from src.application.use_cases.dto.ack_command_dto import AckCommandDTO

from src.domain.command.value_objects import CommandId


class AckCommandUseCase(UseCase):

    def __init__(self, command_repository, uow, outbox):
        super().__init__(uow=uow, outbox=outbox)
        self.command_repository = command_repository

    def execute(self, dto: AckCommandDTO):

        with self.uow:
            command = self.command_repository.get(
                CommandId(dto.command_id)
            )

            if command is None:
                raise ValueError("Command not found")

            command.ack()

            self.commit(command, self.command_repository)

            self.uow.commit()

            return command