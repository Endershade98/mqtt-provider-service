# tests/unit/domain/test_command.py
import pytest

from src.domain.command.entity import Command, CommandStatus
from src.domain.command.events import (
    CommandCreated,
    CommandSent,
    CommandAcknowledged,
    CommandFailed,
)
from src.domain.device.value_objects import CommandId, DeviceId


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
    assert events[0].command_id == "cmd-123"
    assert cmd.status == CommandStatus.PENDING


# ----------------------------------------
# VALID TRANSITIONS
# ----------------------------------------

def test_command_send_valid_transition():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.send()

    events = cmd.pull_events()

    assert cmd.status == CommandStatus.SENT
    assert len(events) == 1
    assert isinstance(events[0], CommandSent)


def test_command_ack_valid_transition():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.send()
    cmd.ack()

    events = cmd.pull_events()

    assert cmd.status == CommandStatus.ACKED
    assert any(isinstance(e, CommandAcknowledged) for e in events)


def test_command_fail_from_pending():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.fail("network error")

    events = cmd.pull_events()

    assert cmd.status == CommandStatus.FAILED
    assert len(events) == 2  # Created + Failed
    assert isinstance(events[-1], CommandFailed)


# ----------------------------------------
# INVALID TRANSITIONS
# ----------------------------------------

def test_cannot_ack_without_send():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    with pytest.raises(ValueError):
        cmd.ack()


def test_cannot_send_twice():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.send()

    with pytest.raises(ValueError):
        cmd.send()


def test_cannot_ack_after_failed():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.fail("error")

    with pytest.raises(ValueError):
        cmd.ack()


# ----------------------------------------
# EVENT METADATA
# ----------------------------------------

def test_event_has_timestamp():
    cmd = Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={}
    )

    cmd.send()

    event = cmd.pull_events()[1]  # second event = CommandSent

    assert event.occurred_at is not None