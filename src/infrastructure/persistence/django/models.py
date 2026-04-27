# src/infrastructure/persistence/django/models.py
from django.db import models
from .base import BaseModel


class DeviceModel(BaseModel):
    id = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=64)
    organization = models.CharField(max_length=64)

    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)

    firmware_version = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        db_table = "devices"

class CommandModel(BaseModel):
    id = models.CharField(primary_key=True, max_length=64)
    device_id = models.CharField(max_length=64)

    payload = models.JSONField()
    status = models.CharField(max_length=32)

    class Meta:
        db_table = "commands"
    
class OutboxModel(BaseModel):
    id = models.AutoField(primary_key=True)

    event_type = models.CharField(max_length=128)
    aggregate_id = models.CharField(max_length=64)

    payload = models.JSONField()

    processed = models.BooleanField(default=False)

    class Meta:
        db_table = "outbox"

