# src/infrastructure/persistence/django/repositories/telemetry_repository.py

from src.domain.device.value_objects import DeviceId
from src.domain.telemetry.entity import Telemetry
from src.infrastructure.persistence.django.models import TelemetryModel
from src.domain.telemetry.repository import TelemetryRepository

class DjangoTelemetryRepository(TelemetryRepository):

    def save(self, telemetry: Telemetry) -> None:
        TelemetryModel.objects.create(
            device_id=(telemetry.device_id.value),
            payload=telemetry.payload,
            received_at=telemetry.received_at,
        )

    def get_all_for_device(self, device_id: DeviceId) -> list[Telemetry]:
        raw_id = device_id.value if hasattr(device_id, "value") else device_id

        qs = (
            TelemetryModel.objects
            .filter(device_id=raw_id)
            .order_by("received_at")
        )

        return [
            Telemetry(
                device_id=DeviceId(row.device_id),
                payload=row.payload,
                received_at=row.received_at,
            )
            for row in qs
        ]