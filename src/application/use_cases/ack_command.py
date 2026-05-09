# src/application/use_cases/ack_command.py

from src.application.ports.outbox import OutboxPort
from src.application.ports.unit_of_work import UnitOfWork
from src.application.use_cases.base import UseCase
from src.application.use_cases.dto.ack_command_dto import AckCommandDTO

from src.domain.command.repository import CommandRepository
from src.domain.command.value_objects import CommandId
from src.application.exceptions import CommandNotFoundError


class AcknowledgeCommandUseCase(UseCase):

    def __init__(self, command_repository:CommandRepository, uow:UnitOfWork, outbox:OutboxPort):
        super().__init__(uow=uow, outbox=outbox)
        self.command_repository = command_repository

    def execute(self, dto: AckCommandDTO):

        with self.uow:

            command = self.command_repository.get(
                CommandId(dto.command_id)
            )

            if command is None:
                raise CommandNotFoundError(dto.command_id)

            command.ack()

            self.commit(command, self.command_repository)

            # OUTBOX EMISSION (CRITICAL FIX)
            self.outbox.save(command.pull_events())

            self.uow.commit()

            return command