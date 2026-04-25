# src/domain/shared/events.py
from dataclasses import dataclass
from datetime import datetime, timezone
import uuid


@dataclass(frozen=True)
class DomainEvent:
    event_id: str
    occurred_at: datetime

    def __init__(self):
        object.__setattr__(self, "event_id", str(uuid.uuid4()))
        object.__setattr__(self, "occurred_at", datetime.now(timezone.utc))