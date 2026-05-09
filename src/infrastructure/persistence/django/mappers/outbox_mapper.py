# src/infrastructure/persistence/django/mappers/outbox_mapper.py

from datetime import datetime
from dataclasses import is_dataclass, asdict


def serialize_event(event) -> dict:
    payload = {}

    data = asdict(event) if is_dataclass(event) else event.__dict__

    for k, v in data.items():

        if hasattr(v, "value"):
            payload[k] = v.value

        elif isinstance(v, datetime):
            payload[k] = v.isoformat()

        elif isinstance(v, (str, int, float, bool)) or v is None:
            payload[k] = v

        else:
            payload[k] = str(v)  # fallback sicuro

    return payload


class OutboxMapper:

    @staticmethod
    def to_record(event, aggregate_id: str) -> dict:
        return {
            "event_type": event.__class__.__name__,
            "aggregate_id": aggregate_id,
            "payload": serialize_event(event),
            "processed": False,
        }