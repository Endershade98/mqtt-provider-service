# src/services/telemetry_service.py
from apps.iot.models import Device, Telemetry, DeviceState
from django.utils import timezone


class TelemetryService:

    def parse_topic(self, topic: str):
        parts = topic.split("/")

        return {
            "device_id": parts[3],
        }


    def handle_telemetry(self, topic: str, payload: dict):
        data = self.parse_topic(topic)
        device_id = data["device_id"]

        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            return

        telemetry = Telemetry.objects.create(
            device=device,
            payload=payload,
            topic=topic
        )

        DeviceState.objects.update_or_create(
            device=device,
            defaults={
                "last_seen": timezone.now(),
                "status": "online"
            }
        )