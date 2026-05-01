# src/infrastructure/persistence/django/mappers/command_mapper.py

from src.domain.command.entity import Command
from src.domain.device.value_objects import DeviceId
from src.domain.command.value_objects import CommandId
from src.infrastructure.persistence.django.models import CommandModel


class CommandMapper:

    @staticmethod
    def to_domain(model: CommandModel) -> Command:
        return Command(
            command_id=CommandId(model.id),
            device_id=DeviceId(model.device_id),
            payload=model.payload,
            status=model.status,
        )

    @staticmethod
    def to_model(entity: Command) -> CommandModel:
        return CommandModel(
            id=entity.command_id.value,
            device_id=entity.device_id.value,
            payload=entity.payload,
            status=entity.status,
        )