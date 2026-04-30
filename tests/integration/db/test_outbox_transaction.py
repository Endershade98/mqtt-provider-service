# tests/integration/db/test_outbox_transaction.py

import pytest
from unittest.mock import patch
from datetime import datetime
from django.utils import timezone
from django.db import transaction

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId

from src.infrastructure.persistence.django.repositories.device_repository import DjangoDeviceRepository
from src.infrastructure.persistence.django.repositories.outbox_repository import DjangoOutboxRepository
from src.infrastructure.persistence.django.models import DeviceModel, OutboxModel


@pytest.mark.django_db
def test_device_and_outbox_saved_atomically():

    repo = DjangoDeviceRepository()
    outbox = DjangoOutboxRepository()

    device = Device(
        id=DeviceId("dev-1"),
        name="test",
        device_type="sensor",
        organization="org"
    )

    device.mark_online(timezone.make_aware(datetime(2024, 1, 1, 12, 0, 0)))
    events = device.pull_events()

    with transaction.atomic():
        repo.save(device)
        outbox.save(events)

    assert DeviceModel.objects.count() == 1
    assert OutboxModel.objects.count() == 1