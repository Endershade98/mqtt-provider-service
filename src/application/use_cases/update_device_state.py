# src/application/use_cases/update_device_state.py

from datetime import datetime

from src.application.use_cases.base import UseCase
from src.application.use_cases.dto.update_device_state_dto import (
    UpdateDeviceStateDTO,
)

from src.domain.device.value_objects import (
    DeviceId,
    DeviceStatus,
)


class UpdateDeviceStateUseCase(UseCase):

    def __init__(self, device_repository, uow, outbox):
        super().__init__(uow=uow, outbox=outbox)
        self.device_repository = device_repository

    def execute(self, dto: UpdateDeviceStateDTO):

        with self.uow:
            device = self.device_repository.get(
                DeviceId(dto.device_id)
            )

            if device is None:
                raise ValueError("Device not found")

            now = datetime.utcnow()

            if dto.target_status == DeviceStatus.ONLINE:
                device.mark_online(now)

            elif dto.target_status == DeviceStatus.OFFLINE:
                device.mark_offline(now)

            elif dto.target_status == DeviceStatus.STALE:
                device.check_stale(
                    now=now,
                    threshold_seconds=0,
                )

            else:
                raise ValueError("Unsupported target status")

            events = self.commit(device, self.device_repository)

            self.uow.commit()

            return events