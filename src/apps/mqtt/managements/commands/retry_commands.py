from django.core.management.base import BaseCommand
from apps.iot.models import Command
from src.services.command_service import retry_command


class Command(BaseCommand):
    help = "Retry failed MQTT commands"

    def handle(self, *args, **kwargs):
        commands = Command.objects.filter(status="failed")

        for cmd in commands:
            retry_command(cmd)

        self.stdout.write(self.style.SUCCESS("Retry completed"))