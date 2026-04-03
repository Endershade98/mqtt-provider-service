from django.utils import timezone
from apps.iot.models import Device, Command
from src.infrastructure.mqtt.publisher import MQTTPublisher

publisher = MQTTPublisher()


def build_command_topic(device: Device, command: str):
    return f"prod/{device.organization}/{device.device_type}/{device.id}/command/{command}"


def send_command(device_id: str, command_name: str, payload: dict):
    device = Device.objects.get(id=device_id)

    command = Command.objects.create(
        device=device,
        command=command_name,
        payload=payload,
        status="pending"
    )

    try:
        topic = build_command_topic(device, command_name)

        publisher.publish(topic, payload)

        command.status = "sent"
        command.sent_at = timezone.now()
        command.save()

    except Exception as e:
        command.status = "failed"
        command.last_error = str(e)
        command.save()

    return command