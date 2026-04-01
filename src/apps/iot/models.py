# src/apps/iot/models.py
import uuid
from django.db import models

class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    # autenticazione
    auth_type = models.CharField(
        max_length=20,
        choices=[
            ("password", "Username/Password"),
            ("certificate", "Certificate"),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)


class DeviceCredential(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    rotated_at = models.DateTimeField(null=True, blank=True)


class DeviceCertificate(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    certificate = models.TextField()  # PEM
    fingerprint = models.CharField(max_length=128, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Telemetry(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()
    topic = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=["device", "timestamp"]),
        ]

class Command(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    command = models.CharField(max_length=100)
    payload = models.JSONField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("sent", "Sent"),
            ("ack", "Acknowledged"),
            ("failed", "Failed"),
        ],
        default="pending"
    )

    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)

    last_error = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

class DeviceState(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)
    firmware_version = models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)