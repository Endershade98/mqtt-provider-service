# src/infrastructure/persistence/django/mappers/outbox_mapper.py

from datetime import datetime


def serialize_event(event):
    payload = {}

    for k, v in event.__dict__.items():

        # Value Objects
        if hasattr(v, "value"):
            payload[k] = v.value

        # datetime
        elif isinstance(v, datetime):
            payload[k] = v.isoformat()

        else:
            payload[k] = v

    return {
        "type": event.__class__.__name__,
        "payload": payload
    }


class OutboxMapper:

    @staticmethod
    def from_event(event, aggregate_id: str):
        return {
            "event_type": event.__class__.__name__,
            "aggregate_id": aggregate_id,
            "payload": serialize_event(event),
        }