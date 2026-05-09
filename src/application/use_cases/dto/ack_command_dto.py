# src/application/use_cases/dto/ack_command_dto.py

from dataclasses import dataclass


@dataclass(frozen=True)
class AckCommandDTO:
    command_id: str