# src/infrastructure/persistence/django/repositories/telemetry_repository.py

from src.domain.device.value_objects import DeviceId
from src.domain.telemetry.entity import Telemetry
from src.infrastructure.persistence.django.models import TelemetryModel


class DjangoTelemetryRepository:

    def save(self, telemetry: Telemetry) -> None:
        TelemetryModel.objects.create(
            device_id=telemetry.device_id.value,
            payload=telemetry.payload,
            received_at=telemetry.received_at,
        )

    def get_all_for_device(self, device_id: DeviceId) -> list[Telemetry]:
        qs = TelemetryModel.objects.filter(
            device_id=device_id.value
        ).order_by("received_at")

        return [
            Telemetry(
                device_id=DeviceId(row.device_id),
                payload=row.payload,
                received_at=row.received_at,
            )
            for row in qs
        ]