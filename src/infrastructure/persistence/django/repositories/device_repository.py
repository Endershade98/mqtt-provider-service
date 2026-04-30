# src/infrastructure/persistence/django/repositories.py

from src.domain.device.repository import DeviceRepository
from src.domain.device.value_objects import DeviceId

from src.infrastructure.persistence.django.models import DeviceModel
from src.infrastructure.persistence.django.mappers.device_mapper import DeviceMapper

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