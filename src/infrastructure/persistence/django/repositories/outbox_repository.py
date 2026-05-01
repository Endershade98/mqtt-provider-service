# src/infrastructure/persistence/django/repositories/outbox_repository.py

from src.application.ports.outbox import OutboxPort
from src.infrastructure.persistence.django.models import OutboxModel


class DjangoOutboxRepository(OutboxPort):

    def save(self, events: list) -> None:
        if not events:
            return

        rows = []

        for event in events:
            rows.append(
                OutboxModel(
                    event_type=event.__class__.__name__,
                    aggregate_id=self._get_aggregate_id(event),
                    payload=self._serialize(event),
                    processed=False,
                )
            )

        # Faster + cleaner than create() in loop
        OutboxModel.objects.bulk_create(rows)

    def get_all(self):
        return list(
            OutboxModel.objects.all().order_by("id")
        )

    def get_unprocessed(self):
        return list(
            OutboxModel.objects.filter(processed=False).order_by("id")
        )

    def mark_processed(self, outbox_id: int) -> None:
        OutboxModel.objects.filter(id=outbox_id).update(processed=True)

    # -----------------------------------------
    # Internal helpers
    # -----------------------------------------

    def _serialize(self, event) -> dict:
        payload = {}

        for key, value in event.__dict__.items():

            # Value Object support
            if hasattr(value, "value"):
                payload[key] = value.value

            # datetime support
            elif hasattr(value, "isoformat"):
                payload[key] = value.isoformat()

            else:
                payload[key] = value

        return payload

    def _get_aggregate_id(self, event) -> str:
        """
        Try common aggregate identifiers.
        """
        for attr in ("device_id", "command_id", "aggregate_id"):

            if hasattr(event, attr):
                value = getattr(event, attr)

                if hasattr(value, "value"):
                    return value.value

                return str(value)

        return ""