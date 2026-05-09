# src/application/use_cases/send_command.py

from src.application.use_cases.base import UseCase
from src.application.use_cases.dto.send_command_dto import SendCommandDTO

from src.domain.command.entity import Command
from src.domain.command.value_objects import CommandId
from src.domain.device.value_objects import DeviceId


class SendCommandUseCase(UseCase):

    def __init__(self, command_repository, uow, outbox):
        super().__init__(uow=uow, outbox=outbox)
        self.command_repository = command_repository

    def execute(self, dto: SendCommandDTO):

        with self.uow:
            command = Command.create(
                command_id=CommandId(dto.command_id),
                device_id=DeviceId(dto.device_id),
                payload=dto.payload,
            )

            command.send()

            self.commit(command, self.command_repository)

            self.uow.commit()

            return command