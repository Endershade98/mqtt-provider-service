# src/infrastructure/persistence/django/repositories/device_repository.py

from src.domain.device.repository import DeviceRepository
from src.domain.device.value_objects import DeviceId
from src.infrastructure.persistence.django.models import DeviceModel
from src.infrastructure.persistence.django.mappers.device_mapper import DeviceMapper


class DjangoDeviceRepository(DeviceRepository):

    def get(self, device_id: DeviceId):
        try:
            row = DeviceModel.objects.get(id=device_id.value)
        except DeviceModel.DoesNotExist:
            return None

        return DeviceMapper.to_domain(row)

    def save(self, device):
        model = DeviceMapper.to_model(device)

        DeviceModel.objects.update_or_create(
            id=model.id,
            defaults={
                "name": model.name,
                "device_type": model.device_type,
                "organization": model.organization,
                "is_online": model.is_online,
                "is_active": model.is_active,
                "last_seen": model.last_seen,
                "firmware_version": model.firmware_version,
            }
        )