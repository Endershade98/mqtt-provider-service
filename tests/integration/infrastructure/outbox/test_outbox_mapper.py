# tests/integration/infrastructure/outbox/test_outbox_mapper.py

import pytest
from datetime import datetime

from src.domain.device.events import DeviceBecameOnline
from src.infrastructure.persistence.django.mappers.outbox_mapper import OutboxMapper


def test_outbox_mapper_serializes_event():
    event = DeviceBecameOnline(
        device_id="dev-1",
        occurred_at=datetime(2026, 1, 1, 10, 0, 0),
    )

    row = OutboxMapper.to_record(event, aggregate_id="dev-1")

    assert row["event_type"] == "DeviceBecameOnline"
    assert row["aggregate_id"] == "dev-1"
    assert row["processed"] is False
    assert row["payload"]["device_id"] == "dev-1"
    assert "occurred_at" in row["payload"]