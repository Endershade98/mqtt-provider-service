# src/domain/device/value_objects.py
from dataclasses import dataclass
from enum import Enum

from src.domain.shared.value_objects import ValueObject
from src.domain.shared.exceptions import InvalidDeviceId, InvalidTopicFormat


class TopicChannel(str, Enum):
    TELEMETRY = "telemetry"
    COMMAND = "commands"
    ACK = "ack"


@dataclass(frozen=True)
class DeviceId(ValueObject):
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or not self.value.strip():
            raise InvalidDeviceId("DeviceId cannot be empty")


@dataclass(frozen=True)
class CommandId(ValueObject):
    value: str


@dataclass(frozen=True)
class Topic(ValueObject):
    """
    iot/devices/{device_id}/{channel}
    """

    value: str

    def __post_init__(self):
        parts = self.value.split("/")

        if len(parts) < 3:
            raise InvalidTopicFormat(self.value)

        # convenzione: channel = ultimo segmento
        channel = parts[-1]

        # device_id = penultimo
        device_id = parts[-2]

        # tutto il resto è "namespace"
        namespace = parts[:-2]

        try:
            topic_channel = TopicChannel(channel)
        except ValueError:
            raise InvalidTopicFormat(f"Unknown channel: {channel}")

        object.__setattr__(self, "_device_id", DeviceId(device_id))
        object.__setattr__(self, "_channel", topic_channel)
        object.__setattr__(self, "_namespace", namespace)

    # ------------------------
    # ACCESSORS
    # ------------------------

    def get_device_id(self) -> DeviceId:
        return self._device_id

    def get_channel(self) -> TopicChannel:
        return self._channel
    # ------------------------
    # BACKWARD COMPATIBILITY
    # ------------------------

    def extract_device_id(self) -> str:
        return self._device_id.value

    # ------------------------
    # HELPERS (semantic routing)
    # ------------------------

    def is_telemetry(self) -> bool:
        return self._channel == TopicChannel.TELEMETRY

    def is_command(self) -> bool:
        return self._channel == TopicChannel.COMMAND

    def is_ack(self) -> bool:
        return self._channel == TopicChannel.ACK