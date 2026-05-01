# src/application/use_cases/send_command.py

from src.domain.command.entity import Command
from src.domain.device.value_objects import DeviceId
from src.domain.command.value_objects import CommandId
from django.db import transaction

class SendCommandUseCase:

    def __init__(self, command_repository, outbox_repository, mqtt_publisher):
        self.command_repository = command_repository
        self.outbox_repository = outbox_repository
        self.mqtt_publisher = mqtt_publisher
    
    @transaction.atomic
    def execute(self, dto):

        command = Command.create(
            command_id=CommandId(dto.command_id),
            device_id=DeviceId(dto.device_id),
            payload=dto.payload
        )

        command.send()

        self.command_repository.save(command)
        self.outbox_repository.save(command.pull_events())

        self.mqtt_publisher.publish(
            topic=f"devices/{dto.device_id}/command",
            payload={
                "command_id": dto.command_id,
                "payload": dto.payload,
                "status": "sent"
            }
        )

        return command