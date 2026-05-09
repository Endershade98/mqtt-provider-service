# src/infrastructure/persistence/django/mappers/device_mapper.py

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId, DeviceStatus
from src.infrastructure.persistence.django.models import DeviceModel


class DeviceMapper:

    @staticmethod
    def to_domain(model: DeviceModel) -> Device:
        status = (
            DeviceStatus.ONLINE
            if model.is_online
            else DeviceStatus.OFFLINE
        )

        return Device(
            id=DeviceId(model.id),
            name=model.name,
            device_type=model.device_type,
            organization=model.organization,
            status=status,
            is_active=model.is_active,
            last_seen=model.last_seen,
            firmware_version=model.firmware_version,
        )

    @staticmethod
    def to_model(entity: Device) -> DeviceModel:
        return DeviceModel(
            id=entity.id.value,
            name=entity.name,
            device_type=entity.device_type,
            organization=entity.organization,
            is_online=entity.status == DeviceStatus.ONLINE,
            is_active=entity.is_active,
            last_seen=entity.last_seen,
            firmware_version=entity.firmware_version,
        )