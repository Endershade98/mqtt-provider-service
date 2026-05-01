# src/application/ports/outbox.py

from abc import ABC, abstractmethod

class OutboxPort(ABC):

    @abstractmethod
    def save(self, events: list):
        pass