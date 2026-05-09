# src/infrastructure/persistence/django/repositories/outbox_repository.py

from src.infrastructure.persistence.django.models import OutboxModel
from src.infrastructure.persistence.django.mappers.outbox_mapper import OutboxMapper


class DjangoOutboxRepository:

    def _get_aggregate_id(self, event):
        return getattr(event, "device_id", None) or getattr(event, "command_id", "unknown")

    def save(self, events):

        rows = [
            OutboxModel(**OutboxMapper.to_record(event, aggregate_id=self._get_aggregate_id(event)))
            for event in events
        ]

        OutboxModel.objects.bulk_create(rows)