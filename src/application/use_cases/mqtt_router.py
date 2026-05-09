# src/application/use_cases/mqtt_router.py


class MQTTApplicationRouter:

    def __init__(self, telemetry_uc, ack_uc):
        self.telemetry_uc = telemetry_uc
        self.ack_uc = ack_uc

    def handle_telemetry(self, dto):
        return self.telemetry_uc.execute(dto)

    def handle_ack(self, dto):
        return self.ack_uc.execute(dto)