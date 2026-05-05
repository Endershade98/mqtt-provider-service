# tests/unit/domain/command/test_command.py

import pytest

from src.domain.command.entity import Command
from src.domain.command.events import (
    CommandCreated,
    CommandSent,
    CommandAcknowledged,
    CommandFailed,
)
from src.domain.command.value_objects import CommandStatus, CommandId
from src.domain.device.value_objects import DeviceId
from src.domain.shared.exceptions import InvalidStateTransition


def make_command():
    return Command.create(
        command_id=CommandId("cmd-123"),
        device_id=DeviceId("dev-456"),
        payload={"action": "restart"},
    )


# ----------------------------------
# CREATION
# ----------------------------------

def test_command_creation_emits_event():
    cmd = make_command()

    events = cmd.pull_events()

    assert cmd.status == CommandStatus.PENDING
    assert len(events) == 1
    assert isinstance(events[0], CommandCreated)


# ----------------------------------
# SEND
# ----------------------------------

def test_command_send_valid_transition():
    cmd = make_command()

    cmd.send()

    events = cmd.pull_events()

    assert cmd.status == CommandStatus.SENT
    assert any(isinstance(e, CommandSent) for e in events)


def test_command_send_twice_fails():
    cmd = make_command()

    cmd.send()

    with pytest.raises(InvalidStateTransition):
        cmd.send()


# ----------------------------------
# ACK
# ----------------------------------

def test_command_ack_after_send():
    cmd = make_command()

    cmd.send()
    cmd.ack()

    events = cmd.pull_events()

    assert cmd.status == CommandStatus.ACKED
    assert any(isinstance(e, CommandAcknowledged) for e in events)


def test_command_ack_without_send_fails():
    cmd = make_command()

    with pytest.raises(InvalidStateTransition):
        cmd.ack()


# ----------------------------------
# FAIL
# ----------------------------------

def test_command_can_fail_from_pending():
    cmd = make_command()

    cmd.fail("network error")

    assert cmd.status == CommandStatus.FAILED


def test_command_can_fail_from_sent():
    cmd = make_command()

    cmd.send()
    cmd.fail("timeout")

    assert cmd.status == CommandStatus.FAILED


def test_acked_command_cannot_fail():
    cmd = make_command()

    cmd.send()
    cmd.ack()

    with pytest.raises(InvalidStateTransition):
        cmd.fail("late failure")