# src/infrastructure/mqtt/publisher.py

from src.domain.command.entity import Command


class MqttPublisher:

    def publish_command(self, command: Command):

        topic = f"devices/{command.device_id.value}/command"

        payload = {
            "command_id": command.command_id.value,
            "device_id": command.device_id.value,
            "payload": command.payload,
            "status": command.status.value
        }

        self.publish(topic, payload)