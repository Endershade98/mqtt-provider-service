# tests/integration/mqtt/test_telemetry_flow.py

import pytest
from django.utils import timezone
from datetime import datetime

from src.interfaces.mqtt.handlers import MQTTHandler
from src.domain.device.entity import Device
from src.domain.device.value_objects import DeviceId


@pytest.mark.django_db
def test_mqtt_telemetry_flow(
    device_repository,
    telemetry_repository,
    outbox_repository
):

    # 1. Setup device IN DB (NON factory)
    device = Device(
        id=DeviceId("device123"),
        name="test",
        device_type="sensor",
        organization="org",
        last_seen=timezone.now()   # 👈 FIX WARNING DeviceModel
    )

    device_repository.save(device)

    # 2. Use case
    from src.application.use_cases.handle_telemetry import HandleTelemetryUseCase

    use_case = HandleTelemetryUseCase(
        device_repository=device_repository,
        telemetry_repository=telemetry_repository,
        outbox_repository=outbox_repository
    )

    # 3. MQTT translator + handler
    from src.interfaces.mqtt.translator import MQTTMessageTranslator

    translator = MQTTMessageTranslator()

    handler = MQTTHandler(
        telemetry_uc=use_case,
        ack_uc=None,
        translator=translator
    )

    # 4. Simulate MQTT message
    topic = "iot/devices/device123/telemetry"
    payload = {"temp": 25}

    handler.handle(topic, payload)

    # 5. Assertions DB state
    updated_device = device_repository.get(DeviceId("device123"))

    assert updated_device.last_seen is not None

    # 6. Telemetry saved
    saved = telemetry_repository.get_all_for_device(DeviceId("device123"))
    assert len(saved) == 1
    assert saved[0].payload == {"temp": 25}

    # 7. Outbox event exists
    events = outbox_repository.get_all()
    assert len(events) >= 1