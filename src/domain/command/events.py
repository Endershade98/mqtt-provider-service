# src/domain/command/events.py
from dataclasses import dataclass
from src.domain.shared.events import DomainEvent


@dataclass(frozen=True)
class CommandCreated(DomainEvent):
    command_id: str

@dataclass(frozen=True)
class CommandSent(DomainEvent):
    command_id: str
    
@dataclass(frozen=True)
class CommandAcknowledged(DomainEvent):
    command_id: str

@dataclass(frozen=True)
class CommandFailed(DomainEvent):
    command_id: str
    reason: str