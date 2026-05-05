# src/application/use_cases/handle_telemetry.py

from src.application.use_cases.base import UseCase
from src.application.use_cases.dto.handle_telemetry_dto import HandleTelemetryDTO

from src.domain.device.value_objects import DeviceId
from src.domain.telemetry.entity import Telemetry


class HandleTelemetryUseCase(UseCase):

    def __init__(
        self,
        device_repository,
        telemetry_repository,
        uow,
        outbox,
    ):
        super().__init__(uow=uow, outbox=outbox)

        self.device_repository = device_repository
        self.telemetry_repository = telemetry_repository

    def execute(self, dto: HandleTelemetryDTO):

        with self.uow:
            device = self.device_repository.get(
                DeviceId(dto.device_id)
            )

            if device is None:
                raise ValueError("Device not found")

            telemetry = Telemetry(
                device_id=device.id,
                payload=dto.payload,
                received_at=dto.received_at,
            )

            device.record_heartbeat(dto.received_at)

            self.telemetry_repository.save(telemetry)

            self.commit(device, self.device_repository)

            self.uow.commit()

            return telemetry