# src/application/use_cases/mqtt_router.py

from src.application.use_cases.handle_telemetry import HandleTelemetryUseCase
from src.application.use_cases.ack_command import AcknowledgeCommandUseCase
from src.application.use_cases.dto.handle_telemetry_dto import HandleTelemetryDTO
from src.application.use_cases.dto.ack_command_dto import AckCommandDTO


class MQTTApplicationRouter:

    def __init__(
        self,
        telemetry_uc: HandleTelemetryUseCase,
        ack_uc: AcknowledgeCommandUseCase,
    ):
        self.telemetry_uc = telemetry_uc
        self.ack_uc = ack_uc

    def handle_telemetry(self, dto: HandleTelemetryDTO):
        return self.telemetry_uc.execute(dto)

    def handle_ack(self, dto: AckCommandDTO):
        return self.ack_uc.execute(dto)