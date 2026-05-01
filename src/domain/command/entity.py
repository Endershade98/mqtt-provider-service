# src/domain/command/entity.py

from dataclasses import dataclass, field
from typing import List

from src.domain.command.events import (
    CommandCreated,
    CommandSent,
    CommandAcknowledged,
    CommandFailed
)
from src.domain.device.value_objects import DeviceId
from src.domain.command.value_objects import CommandStatus, CommandId
from src.domain.shared.exceptions import InvalidStateTransition


ALLOWED_TRANSITIONS = {
    CommandStatus.PENDING: [CommandStatus.SENT, CommandStatus.FAILED],
    CommandStatus.SENT: [CommandStatus.ACKED, CommandStatus.FAILED],
    CommandStatus.ACKED: [],
    CommandStatus.FAILED: [],
}

@dataclass(frozen=True)
class Command:
    command_id: CommandId
    device_id: DeviceId
    payload: dict
    status: CommandStatus = CommandStatus.PENDING

    _events: List = field(default_factory=list, init=False)

    def _ensure_transition(self, new_status: CommandStatus):
        allowed = ALLOWED_TRANSITIONS[self.status]

        if new_status not in allowed:
            raise InvalidStateTransition(
                f"Invalid transition from {self.status} to {new_status}"
            )

    def send(self):
        self._ensure_transition(CommandStatus.SENT)

        self.status = CommandStatus.SENT

        self._events.append(
            CommandSent(command_id=self.command_id.value)
        )

    def ack(self):
        self._ensure_transition(CommandStatus.ACKED)

        self.status = CommandStatus.ACKED

        self._events.append(
            CommandAcknowledged(command_id=self.command_id.value)
        )

    def fail(self, reason: str):
        self._ensure_transition(CommandStatus.FAILED)

        self.status = CommandStatus.FAILED

        self._events.append(
            CommandFailed(
                command_id=self.command_id.value,
                reason=reason
            )
        )
    
    @classmethod
    def create(cls, command_id, device_id, payload):
        cmd = cls(
            command_id=command_id,
            device_id=device_id,
            payload=payload,
            status=CommandStatus.PENDING
        )

        cmd._events.append(
            CommandCreated(command_id=command_id.value)
        )

        return cmd
    
    def pull_events(self) -> List:
        events = self._events[:]
        self._events.clear()
        return events