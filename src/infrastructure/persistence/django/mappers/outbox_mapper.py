# src/infrastructure/persistence/django/mappers/outbox_mapper.py
import json
from datetime import datetime
from src.infrastructure.persistence.django.models import OutboxModel


def serialize_event(event):
    payload = event.__dict__.copy()

    # converti datetime -> ISO string
    for k, v in payload.items():
        if isinstance(v, datetime):
            payload[k] = v.isoformat()

    return {
        "type": event.__class__.__name__,
        "payload": payload
    }

class OutboxMapper:

    @staticmethod
    def from_event(event, aggregate_id: str) -> OutboxModel:
        return OutboxModel(
            event_type=event.__class__.__name__,
            aggregate_id=aggregate_id,
            payload=event.__dict__,
        )