# tests/integration/db/test_outbox.py

import pytest

from datetime import datetime
from django.utils import timezone

from src.domain.device.entity import Device
from src.domain.device.events import DeviceBecameOffline, DeviceBecameOnline
from src.domain.device.value_objects import DeviceId

from src.infrastructure.persistence.django.repositories.device_repository import DjangoDeviceRepository
from src.infrastructure.persistence.django.repositories.outbox_repository import DjangoOutboxRepository
from src.infrastructure.persistence.django.models import OutboxModel


@pytest.mark.django_db
def test_outbox_is_written_on_device_save():

    repo = DjangoDeviceRepository()
    outbox = DjangoOutboxRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org"
    )

    device.mark_online(timezone.make_aware(datetime(2024, 1, 1, 12, 0, 0)))
    events = device.pull_events()

    repo.save(device)
    outbox.save(events)

    assert OutboxModel.objects.count() == 1

    event = OutboxModel.objects.first()
    assert event.event_type == "DeviceBecameOnline"
    assert event.aggregate_id == "dev-1"

def test_outbox_with_no_events():
    repo = DjangoOutboxRepository()

    repo.save([])

    assert OutboxModel.objects.count() == 0

def test_outbox_multiple_events_saved():
    repo = DjangoOutboxRepository()

    events = [
        DeviceBecameOnline(device_id="dev-1", occurred_at=timezone.now()),
        DeviceBecameOffline(device_id="dev-1", occurred_at=timezone.now()),
    ]

    repo.save(events)

    assert OutboxModel.objects.count() == 2

def test_outbox_idempotency_behavior():
    repo = DjangoOutboxRepository()

    events = [
        DeviceBecameOnline(device_id="dev-1", occurred_at=timezone.now())
    ]

    repo.save(events)
    repo.save(events)

    # definisci comportamento atteso (importantissimo)
    assert OutboxModel.objects.count() == 2  # oppure 1 se vuoi dedup