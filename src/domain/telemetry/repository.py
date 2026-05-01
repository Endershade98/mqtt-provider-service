# src/domain/telemetry/repository.py

from abc import ABC, abstractmethod
from typing import List
from src.domain.telemetry.entity import Telemetry


class TelemetryRepository(ABC):

    @abstractmethod
    def save(self, telemetry: Telemetry) -> None:
        """
        Persist a single telemetry record
        """
        pass

    @abstractmethod
    def save_batch(self, telemetry_list: List[Telemetry]) -> None:
        """
        Optional batch insert for high throughput
        """
        pass