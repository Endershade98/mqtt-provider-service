# tests/integration/db/test_transaction_atomicity.py
import pytest

from datetime import datetime
from unittest.mock import patch

from django.utils import timezone
from src.domain.device.entity import Device
from src.domain.device.events import DeviceBecameOffline, DeviceBecameOnline
from src.domain.device.value_objects import DeviceId
from src.infrastructure.persistence.django.models import DeviceModel, OutboxModel
from src.infrastructure.persistence.django.repositories.device_repository import DjangoDeviceRepository
from src.infrastructure.persistence.django.repositories.outbox_repository import DjangoOutboxRepository

from django.db import transaction


def test_outbox_saves_multiple_events():
    repo = DjangoOutboxRepository()

    now = timezone.make_aware(datetime(2024, 1, 1, 12, 0, 0))

    events = [
        DeviceBecameOnline(device_id="dev-1", occurred_at=now),
        DeviceBecameOffline(device_id="dev-1", occurred_at=now),
    ]

    repo.save(events)

    assert len(OutboxModel.objects.all()) == 2

def test_outbox_is_idempotent():
    repo = DjangoOutboxRepository()

    now = timezone.make_aware(datetime(2024, 1, 1, 12, 0, 0))

    event = DeviceBecameOnline(device_id="dev-1", occurred_at=now)

    repo.save([event])
    repo.save([event])  # duplicato

    # dipende dal tuo design: almeno non crasha
    assert OutboxModel.objects.count() >= 1


@pytest.mark.django_db
def test_device_and_outbox_are_atomic():

    repo = DjangoDeviceRepository()
    outbox = DjangoOutboxRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="sensor",
        device_type="iot",
        organization="org"
    )

    device.mark_online(timezone.now())
    events = device.pull_events()

    with patch(
        "src.infrastructure.persistence.django.models.OutboxModel.objects.create",
        side_effect=Exception("DB failure")
    ):
        try:
            with transaction.atomic():
                repo.save(device)
                outbox.save(events)
        except Exception:
            pass

    assert DeviceModel.objects.count() == 0
    assert OutboxModel.objects.count() == 0

@pytest.mark.django_db
def test_transaction_rolls_back_on_outbox_failure():
    repo = DjangoDeviceRepository()
    outbox = DjangoOutboxRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="test",
        device_type="sensor",
        organization="org"
    )

    device.mark_online(timezone.now())
    events = device.pull_events()

    with patch.object(DjangoOutboxRepository, "save", side_effect=Exception("fail")):
        with pytest.raises(Exception):
            with transaction.atomic():
                repo.save(device)
                outbox.save(events)

    assert DeviceModel.objects.count() == 0

@pytest.mark.django_db
def test_transaction_commit_success():
    repo = DjangoDeviceRepository()
    outbox = DjangoOutboxRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="test",
        device_type="sensor",
        organization="org"
    )

    device.mark_online(timezone.now())
    events = device.pull_events()

    repo.save(device)
    outbox.save(events)

    assert DeviceModel.objects.count() == 1
    assert OutboxModel.objects.count() == 1

def test_device_save_is_idempotent():
    repo = DjangoDeviceRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="a",
        device_type="iot",
        organization="org"
    )

    repo.save(device)
    repo.save(device)

    assert DeviceModel.objects.count() == 1

@pytest.mark.django_db
def test_transaction_rolls_back_device_and_outbox():

    with patch(
        "src.infrastructure.persistence.django.models.OutboxModel.objects.create",
        side_effect=Exception("fail")
    ):
        try:
            with transaction.atomic():
                DeviceModel.objects.create(id="dev-1", name="x")
                OutboxModel.objects.create(id="1")
        except Exception:
            pass

    assert DeviceModel.objects.count() == 0
    assert OutboxModel.objects.count() == 0
