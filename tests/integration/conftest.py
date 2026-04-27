# tests/integration/conftest.py
import os
import django
import pytest

from src.infrastructure.persistence.django.models import DeviceModel, OutboxModel

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

@pytest.fixture(autouse=True)
def clean_db(db):
    DeviceModel.objects.all().delete()
    OutboxModel.objects.all().delete()