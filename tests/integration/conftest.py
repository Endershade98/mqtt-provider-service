# tests/integration/conftest.py

import os
import django
import pytest

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId

from src.infrastructure.persistence.django.models import (
    DeviceModel,
    OutboxModel,
    TelemetryModel,   # 👈 AGGIUNGI
)

from src.infrastructure.persistence.django.repositories.device_repository import DjangoDeviceRepository
from src.infrastructure.persistence.django.repositories.outbox_repository import DjangoOutboxRepository
from src.infrastructure.persistence.django.repositories.telemetry_repository import DjangoTelemetryRepository  # 👈 AGGIUNGI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


@pytest.fixture(autouse=True)
def clean_db(db):
    DeviceModel.objects.all().delete()
    OutboxModel.objects.all().delete()
    TelemetryModel.objects.all().delete()   # 👈 AGGIUNGI


@pytest.fixture
def device_factory():
    def create(**kwargs):
        return Device(
            id=DeviceId(kwargs.get("id", "device123")),
            name="test",
            device_type="sensor",
            organization="org"
        )
    return create


# =========================
# REPOSITORIES (REALI)
# =========================

@pytest.fixture
def device_repository():
    return DjangoDeviceRepository()


@pytest.fixture
def outbox_repository():
    return DjangoOutboxRepository()


@pytest.fixture
def telemetry_repository():
    return DjangoTelemetryRepository()