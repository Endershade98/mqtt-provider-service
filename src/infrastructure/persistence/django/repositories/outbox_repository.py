# src/infrastructure/persistence/django/repositories/outbox_repository.py

from src.infrastructure.persistence.django.models import OutboxModel


class DjangoOutboxRepository:

    def save(self, events: list):
        from django.db import transaction

        with transaction.atomic():
            for event in events:
                OutboxModel.objects.create(
                    event_type=event.__class__.__name__,
                    aggregate_id=self._get_aggregate_id(event),
                    payload=self._serialize(event),
                    processed=False,
                )

    def get_all(self):
        return list(OutboxModel.objects.all())

    def _serialize(self, event):
        payload = event.__dict__.copy()

        # VO + datetime safe handling
        for k, v in payload.items():
            if hasattr(v, "value"):
                payload[k] = v.value
            elif hasattr(v, "isoformat"):
                payload[k] = v.isoformat()

        return payload

    def _get_aggregate_id(self, event):
        if hasattr(event, "device_id"):
            device_id = event.device_id
            return device_id.value if hasattr(device_id, "value") else device_id
        return ""