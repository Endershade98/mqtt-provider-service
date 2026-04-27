# src/infrastructure/persistence/django/outbox_repository.py
from src.application.ports.outbox import OutboxPort
from src.infrastructure.persistence.django.models import OutboxModel
from .mappers.outbox_mapper import serialize_event
from django.db import transaction

class DjangoOutboxRepository(OutboxPort):

    def save(self, events: list):
        with transaction.atomic():
            for event in events:
                OutboxModel.objects.create(
                    event_type=event.__class__.__name__,
                    aggregate_id=self._get_aggregate_id(event),
                    payload=serialize_event(event),
                    processed=False,
                )

    def _get_aggregate_id(self, event):

        if hasattr(event, "device_id"):
            device_id = event.device_id

            # Value Object case
            if hasattr(device_id, "value"):
                return device_id.value

            # string case
            return device_id

        return ""