# src/application/use_cases/dto/update_device_state_dto.py

from dataclasses import dataclass
from src.domain.device.value_objects import DeviceStatus


@dataclass(frozen=True)
class UpdateDeviceStateDTO:
    device_id: str
    target_status: DeviceStatus