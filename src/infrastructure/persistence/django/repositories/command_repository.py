# src/infrastructure/persistence/django/repositories/command_repository.py

from src.domain.device.repository import DeviceRepository
from src.domain.command.repository import CommandRepository
from src.domain.device.value_objects import CommandId

from src.infrastructure.persistence.django.models import CommandModel
from src.infrastructure.persistence.django.mappers.command_mapper import CommandMapper


from django.db import transaction


class DjangoCommandRepository(CommandRepository):

    def get(self, command_id: CommandId):
        model = CommandModel.objects.get(id=command_id.value)
        return CommandMapper.to_domain(model)

    def save(self, command):
        model = CommandMapper.to_model(command)

        CommandModel.objects.update_or_create(
            id=model.id,
            defaults={
                "device_id": model.device_id,
                "payload": model.payload,
                "status": model.status,
            }
        )