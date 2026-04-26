# src/domain/command/events.py
from dataclasses import dataclass


@dataclass(frozen=True)
class CommandCreated:
    command_id: str

@dataclass(frozen=True)
class CommandSent:
    command_id: str
    
@dataclass(frozen=True)
class CommandAcknowledged:
    command_id: str

@dataclass(frozen=True)
class CommandFailed:
    command_id: str
    reason: str