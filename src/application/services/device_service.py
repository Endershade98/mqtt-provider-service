# src/application/services/device_service.py
from src.domain.device.entity import Device
from src.domain.telemetry.entity import Telemetry


class DeviceService:
    def record_telemetry(self, device: Device, telemetry: Telemetry):
        device.mark_online(telemetry.received_at)
        return device