# tests/unit/domain/command/test_command_state_machine.py

import pytest

from src.domain.command.entity import Command
from src.domain.command.value_objects import CommandStatus, CommandId
from src.domain.device.value_objects import DeviceId
from src.domain.shared.exceptions import InvalidStateTransition


def make_command():
    return Command.create(
        command_id=CommandId("cmd-1"),
        device_id=DeviceId("device123"),
        payload={"action": "reboot"}
    )


# ----------------------------------
# RETRY
# ----------------------------------

def test_failed_command_can_retry():
    cmd = make_command()

    cmd.fail("timeout")
    cmd.retry()

    assert cmd.status == CommandStatus.RETRYING
    assert cmd.retry_count == 1


def test_retry_can_be_sent_again():
    cmd = make_command()

    cmd.fail("timeout")
    cmd.retry()
    cmd.send()

    assert cmd.status == CommandStatus.SENT


# ----------------------------------
# EXPIRE
# ----------------------------------

def test_failed_command_can_expire():
    cmd = make_command()

    cmd.fail("timeout")
    cmd.expire()

    assert cmd.status == CommandStatus.EXPIRED


# ----------------------------------
# INVALID
# ----------------------------------

def test_acked_command_cannot_retry():
    cmd = make_command()

    cmd.send()
    cmd.ack()

    with pytest.raises(InvalidStateTransition):
        cmd.retry()