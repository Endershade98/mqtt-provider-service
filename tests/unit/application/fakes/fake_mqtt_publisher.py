# tests/unit/application/fakes/fake_mqtt_publisher.py

class FakeMqttPublisher:
    def __init__(self):
        self.published = []

    def publish_command(self, command):
        self.published.append(command)