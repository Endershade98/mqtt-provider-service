# tests/unit/domain/command/test_command_state_machine.py

import pytest

from src.domain.command.entity import Command
from src.domain.command.value_objects import CommandId
from src.domain.device.value_objects import DeviceId


def test_command_cannot_be_sent_twice():

    command = Command.create(
        command_id=CommandId("cmd-1"),
        device_id=DeviceId("device123"),
        payload={"action": "reboot"}
    )

    command.send()

    with pytest.raises(Exception):
        command.send()  # invalid transition


def test_command_idempotency_send():

    command = Command.create(
        command_id=CommandId("cmd-1"),
        device_id=DeviceId("device123"),
        payload={"action": "reboot"}
    )

    command.send()

    assert command.status == "SENT"