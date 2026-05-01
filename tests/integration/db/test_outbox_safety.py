# tests/integration/db/test_outbox_safety.py

import pytest

from src.domain.device.entity import Device

from src.domain.device.value_objects import DeviceId
from src.domain.command.value_objects import CommandId

from src.application.use_cases.send_command import SendCommandUseCase
from src.infrastructure.persistence.django.repositories.command_repository import DjangoCommandRepository


class FakeMqttPublisher:
    def __init__(self):
        self.sent = []

    def publish_command(self, command):
        self.sent.append(command)


@pytest.mark.django_db
def test_outbox_is_saved_with_command(device_repository, outbox_repository):

    device = Device(
        id=DeviceId("device123"),
        name="test-device",
        device_type="sensor",
        organization="org"
    )
    device_repository.save(device)

    command_repository = DjangoCommandRepository()
    mqtt = FakeMqttPublisher()

    use_case = SendCommandUseCase(
        command_repository=command_repository,
        outbox_repository=outbox_repository,
        mqtt_publisher=mqtt
    )

    command = use_case.execute(
        command_id=CommandId("cmd-1"),
        device_id=DeviceId("device123"),
        payload={"action": "reboot"}
    )

    # command salvato
    assert command.status == "SENT"

    # outbox generato
    events = outbox_repository.get_all()
    assert len(events) >= 1

    # mqtt chiamato
    assert len(mqtt.sent) == 1