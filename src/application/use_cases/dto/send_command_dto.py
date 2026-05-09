# src/application/use_cases/dto/send_command_dto.py

from dataclasses import dataclass


@dataclass(frozen=True)
class SendCommandDTO:
    command_id: str
    device_id: str
    payload: dict