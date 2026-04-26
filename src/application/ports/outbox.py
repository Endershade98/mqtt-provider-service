# src/application/ports/outbox.py
from abc import ABC, abstractmethod
from typing import List


class Outbox(ABC):

    @abstractmethod
    def add(self, events: List):
        pass