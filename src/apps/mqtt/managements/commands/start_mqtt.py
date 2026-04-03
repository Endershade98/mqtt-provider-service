# src/apps/mqtt/management/commands/start_mqtt.py
from django.core.management.base import BaseCommand
from src.infrastructure.mqtt.client import MQTTClient


class Command(BaseCommand):
    mqtt_client = MQTTClient()
    help = "Start MQTT worker"

    def handle(self, *args, **kwargs):
        self.mqtt_client.start_mqtt()