# src/application/use_cases/ack_command.py

from dataclasses import dataclass
from django.db import transaction


@dataclass(frozen=True)
class AckCommandDTO:
    device_id: str
    payload: dict


class AckCommandUseCase:

    def __init__(self, command_service):
        self.command_service = command_service

    @transaction.atomic
    def execute(self, dto: AckCommandDTO):

        return self.command_service.ack(
            device_id=dto.device_id,
            payload=dto.payload,
        )