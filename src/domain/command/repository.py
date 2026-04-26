# src/domain/command/repository.py
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.command.entity import Command


class CommandRepository(ABC):

    @abstractmethod
    def get(self, command_id: str) -> Optional[Command]:
        pass

    @abstractmethod
    def save(self, command: Command) -> None:
        pass