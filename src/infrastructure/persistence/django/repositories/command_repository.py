# src/infrastructure/persistence/django/repositories/command_repository.py

from src.domain.command.repository import CommandRepository
from src.domain.command.value_objects import CommandId
from src.application.exceptions import CommandNotFoundError

from src.infrastructure.persistence.django.models import CommandModel
from src.infrastructure.persistence.django.mappers.command_mapper import CommandMapper


class DjangoCommandRepository(CommandRepository):

    def get(self, command_id: CommandId):
        try:
            model = CommandModel.objects.get(id=command_id.value)
        except CommandModel.DoesNotExist:
            return None

        return CommandMapper.to_domain(model)

    def save(self, command):
        model = CommandMapper.to_model(command)

        CommandModel.objects.update_or_create(
            id=model.id,
            defaults={
                "device_id": model.device_id,
                "payload": model.payload,
                "status": model.status.value,
            }
        )