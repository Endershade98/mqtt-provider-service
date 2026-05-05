# src/application/ports/outbox.py

from abc import ABC, abstractmethod
from typing import Iterable


class OutboxPort(ABC):

    @abstractmethod
    def save(self, events: Iterable[object]) -> None:
        """
        Persist domain events atomically with aggregate changes.
        """
        raise NotImplementedError