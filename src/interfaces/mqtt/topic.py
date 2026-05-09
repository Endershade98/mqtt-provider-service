# src/interfaces/mqtt/topic.py

from dataclasses import dataclass
from enum import Enum

from src.domain.device.value_objects import DeviceId
from src.domain.shared.exceptions import InvalidTopicFormat


class TopicChannel(str, Enum):
    TELEMETRY = "telemetry"
    COMMAND = "command"
    ACK = "ack"


@dataclass(frozen=True)
class Topic:
    raw: str

    def __post_init__(self):
        parts = self.raw.split("/")

        if len(parts) < 3:
            raise InvalidTopicFormat(self.raw)

        device_id = parts[-2]
        channel = parts[-1]

        object.__setattr__(self, "_device_id", DeviceId(device_id))
        object.__setattr__(self, "_channel", TopicChannel(channel))

    @property
    def device_id(self) -> DeviceId:
        return self._device_id

    @property
    def channel(self) -> TopicChannel:
        return self._channel