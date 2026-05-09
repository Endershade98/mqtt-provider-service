# src/infrastructure/mqtt/publisher.py

class MqttPublisher:
    """
    Infrastructure adapter for MQTT publishing.
    No domain dependency allowed.
    """

    def publish_command(
        self,
        command_id: str,
        device_id: str,
        payload: dict,
        status: str
    ) -> None:

        topic = f"devices/{device_id}/command"

        message = {
            "command_id": command_id,
            "device_id": device_id,
            "payload": payload,
            "status": status,
        }

        self.publish(topic, message)

    def publish(self, topic: str, payload: dict):
        raise NotImplementedError