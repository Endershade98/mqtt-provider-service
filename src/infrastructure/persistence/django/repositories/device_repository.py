# src/infrastructure/persistence/django/repositories/device_repository.py

from src.domain.device.repository import DeviceRepository
from src.domain.device.value_objects import DeviceId
from src.domain.device.entity import Device
from src.infrastructure.persistence.django.models import DeviceModel
from src.infrastructure.persistence.django.mappers.device_mapper import DeviceMapper
from src.domain.shared.exceptions import DeviceNotFound


class DjangoDeviceRepository(DeviceRepository):

    def get(self, device_id: DeviceId) -> Device:
        try:
            model = DeviceModel.objects.get(id=device_id.value)
        except DeviceModel.DoesNotExist:
            raise DeviceNotFound(f"Device with id {device_id.value} not found")

        return DeviceMapper.to_domain(model)

    def save(self, device: Device) -> None:
        DeviceModel.objects.update_or_create(
            id=device.id.value,
            defaults={
                "name": device.name,
                "device_type": device.device_type,
                "organization": device.organization,
                "is_online": device.is_online,
                "is_active": device.is_active,
                "last_seen": device.last_seen,
                "firmware_version": device.firmware_version,
            }
        )