# src/interfaces/mqtt/message.py

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class MQTTMessage:
    topic: str
    payload: Dict[str, Any]