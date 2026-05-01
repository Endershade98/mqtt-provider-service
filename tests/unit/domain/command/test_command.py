# tests/unit/domain/command/test_command.py

import pytest

from src.domain.command.entity import Command
from src.domain.command.value_objects import CommandStatus, CommandId
from src.domain.device.value_objects import DeviceId
from src.domain.command.events import CommandCreated


# ----------------------------------------
# CREATION
# ----------------------------------------

def test_command_creation_emits_event():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={"action": "restart"},
    )

    events = cmd.pull_events()

    assert len(events) == 1
    assert isinstance(events[0], CommandCreated)
    assert cmd.status == CommandStatus.PENDING


# ----------------------------------------
# SEND
# ----------------------------------------

def test_command_send_valid_transition():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.send()

    assert cmd.status == CommandStatus.SENT


def test_command_send_twice_fails():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.send()

    with pytest.raises(Exception):
        cmd.send()


# ----------------------------------------
# ACK
# ----------------------------------------

def test_command_ack_requires_sent_state():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.send()
    cmd.ack()

    assert cmd.status == CommandStatus.ACKED


def test_command_ack_without_send_fails():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    with pytest.raises(Exception):
        cmd.ack()


# ----------------------------------------
# FAIL
# ----------------------------------------

def test_command_fail_from_any_state():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.fail("error")

    assert cmd.status == CommandStatus.FAILED
    assert len(cmd.pull_events()) >= 1