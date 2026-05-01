# tests/integration/mqtt/test_command_flow.py

import pytest

from src.domain.device.value_objects import DeviceId
from src.domain.command.value_objects import CommandId
from src.domain.device.entity import Device

from src.application.use_cases.send_command import SendCommandUseCase
from src.infrastructure.persistence.django.repositories.command_repository import DjangoCommandRepository


class FakeMqttPublisher:
    def __init__(self):
        self.sent = []

    def publish_command(self, command):
        self.sent.append(command)


@pytest.mark.django_db
def test_send_command_flow(device_repository, outbox_repository):

    device = Device(
        id=DeviceId("device123"),
        name="test-device",
        device_type="sensor",
        organization="org"
    )
    device_repository.save(device)

    command_repository = DjangoCommandRepository()
    mqtt_publisher = FakeMqttPublisher()

    use_case = SendCommandUseCase(
        command_repository=command_repository,
        outbox_repository=outbox_repository,
        mqtt_publisher=mqtt_publisher
    )

    command = use_case.execute(
        command_id=CommandId("cmd-1"),
        device_id=DeviceId("device123"),
        payload={"action": "reboot"}
    )

    assert command.status == "SENT"

    assert len(mqtt_publisher.sent) == 1

    sent_command = mqtt_publisher.sent[0]

    assert sent_command.command_id.value == "cmd-1"
    assert sent_command.device_id.value == "device123"
    assert sent_command.payload["action"] == "reboot"