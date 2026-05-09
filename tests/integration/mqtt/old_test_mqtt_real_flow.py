# tests/integration/mqtt/test_mqtt_real_flow.py

import pytest
from django.utils import timezone

from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId

from src.interfaces.mqtt.handlers import MQTTHandler
from src.interfaces.mqtt.dispatcher import MQTTDispatcher
from src.interfaces.mqtt.translator import MQTTMessageTranslator

from src.application.use_cases.handle_telemetry import HandleTelemetryUseCase

from src.infrastructure.persistence.django.repositories.device_repository import (
    DjangoDeviceRepository,
)
from src.infrastructure.persistence.django.repositories.telemetry_repository import (
    DjangoTelemetryRepository,
)
from src.infrastructure.persistence.django.repositories.outbox_repository import (
    DjangoOutboxRepository,
)
from src.infrastructure.persistence.django.unit_of_work import DjangoUnitOfWork


@pytest.mark.django_db
def test_mqtt_real_flow():
    """
    REAL full integration flow:

    MQTT inbound message
    -> Interface Layer
    -> Application Use Case
    -> Domain logic
    -> Django repositories
    -> SQLite test database
    """

    # -------------------------------------------------
    # REAL INFRASTRUCTURE
    # -------------------------------------------------
    device_repository = DjangoDeviceRepository()
    telemetry_repository = DjangoTelemetryRepository()
    outbox_repository = DjangoOutboxRepository()
    uow = DjangoUnitOfWork()

    # -------------------------------------------------
    # PRELOAD DEVICE
    # -------------------------------------------------
    device = Device(
        id=DeviceId("device123"),
        name="sensor",
        device_type="iot",
        organization="org",
        last_seen=timezone.now(),
    )

    device_repository.save(device)

    # -------------------------------------------------
    # REAL USE CASE
    # -------------------------------------------------
    telemetry_use_case = HandleTelemetryUseCase(
        device_repository=device_repository,
        telemetry_repository=telemetry_repository,
        uow=uow,
        outbox=outbox_repository,
    )

    # -------------------------------------------------
    # REAL MQTT STACK
    # -------------------------------------------------
    translator = MQTTMessageTranslator()

    dispatcher = MQTTDispatcher(
        routes={
            "telemetry": telemetry_use_case,
        }
    )

    handler = MQTTHandler(
        translator=translator,
        dispatcher=dispatcher,
    )

    # -------------------------------------------------
    # MQTT MESSAGE ARRIVES
    # -------------------------------------------------
    now = timezone.now()

    handler.handle(
        topic="devices/device123/telemetry",
        payload={
            "temp": 22,
            "humidity": 60,
        },
        received_at=now,
    )

    # -------------------------------------------------
    # ASSERT TELEMETRY SAVED
    # -------------------------------------------------
    saved = telemetry_repository.get_latest("device123")

    assert saved is not None
    assert saved.device_id.value == "device123"
    assert saved.payload["temp"] == 22
    assert saved.payload["humidity"] == 60

    # -------------------------------------------------
    # ASSERT DEVICE UPDATED
    # -------------------------------------------------
    loaded = device_repository.get(DeviceId("device123"))

    assert loaded is not None
    assert loaded.id.value == "device123"
    assert loaded.last_seen is not None