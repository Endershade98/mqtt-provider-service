# src/interfaces/mqtt/topic_parser.py
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedTopic:
    device_id: str
    message_type: str


class TopicParser:

    @staticmethod
    def parse(topic: str) -> ParsedTopic:
        parts = topic.split("/")

        if len(parts) < 3:
            raise ValueError(f"Invalid topic: {topic}")

        # esempio: devices/{device_id}/telemetry
        return ParsedTopic(
            device_id=parts[1],
            message_type=parts[2],
        )