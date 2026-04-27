# src/infrastructure/persistence/django/repositories.py
from src.application import device
from src.domain.device.repository import DeviceRepository
from src.domain.command.repository import CommandRepository
from src.domain.device.value_objects import DeviceId
from src.domain.device.value_objects import CommandId

from src.infrastructure.persistence.django.models import DeviceModel, CommandModel, OutboxModel
from src.infrastructure.persistence.django.mappers.device_mapper import DeviceMapper
from src.infrastructure.persistence.django.mappers.command_mapper import CommandMapper
from .mappers.outbox_mapper import serialize_event

from django.db import transaction

# ==========================================
# DEVICE REPOSITORY
# ==========================================
class DjangoDeviceRepository(DeviceRepository):

    def get(self, device_id: DeviceId):
        model = DeviceModel.objects.get(id=device_id.value)
        return DeviceMapper.to_domain(model)

    @transaction.atomic
    def save(self, device):
        DeviceModel.objects.update_or_create(
            id=device.id.value,
            defaults={
                "name": device.name,
                "device_type": device.device_type,
                "organization": device.organization,
                "is_online": device.is_online,
                "last_seen": device.last_seen,
            }
        )

# ==========================================
# COMMAND REPOSITORY
# ==========================================

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