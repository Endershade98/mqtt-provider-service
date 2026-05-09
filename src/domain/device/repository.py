# src/domain/device/repository.py

from abc import ABC, abstractmethod
from typing import Optional
from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


class DeviceRepository(ABC):

    @abstractmethod
    def get(self, device_id: DeviceId) -> Optional[Device]:
        pass

    @abstractmethod
    def save(self, device: Device) -> None:
        pass