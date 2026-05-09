# tests/integration/e2e/test_mqtt_ack_flow.py

from datetime import datetime

from src.interfaces.mqtt.handlers import MQTTHandler
from src.interfaces.mqtt.translator import MQTTMessageTranslator
from src.application.use_cases.mqtt_router import MQTTApplicationRouter

from src.application.use_cases.ack_command import AcknowledgeCommandUseCase
from src.application.use_cases.handle_telemetry import HandleTelemetryUseCase
from tests.unit.application.fakes.fake_command_repository import FakeCommandRepository
from tests.unit.application.fakes.fake_device_repository import FakeDeviceRepository
from tests.unit.application.fakes.fake_outbox import FakeOutbox
from tests.unit.application.fakes.fake_unit_of_work import FakeUnitOfWork


class FakeId:
    def __init__(self, value):
        self.value = value


class FakeCommand:
    def __init__(self, command_id="cmd-1"):
        self.command_id = FakeId(command_id)
        self.ack_called = False
        self._events = []

    def ack(self):
        self.ack_called = True
        self._events.append("acked")

    def pull_events(self):
        events = self._events[:]
        self._events.clear()
        return events


def test_mqtt_ack_flow_end_to_end():

    # -------------------------
    # FAKES / INFRA
    # -------------------------
    command_repo = FakeCommandRepository()
    device_repo = FakeDeviceRepository()
    uow = FakeUnitOfWork()
    outbox = FakeOutbox()

    cmd = FakeCommand()
    command_repo.storage["cmd-1"] = cmd

    # -------------------------
    # USE CASES
    # -------------------------
    ack_uc = AcknowledgeCommandUseCase(
        command_repository=command_repo,
        uow=uow,
        outbox=outbox,
    )

    telemetry_uc = HandleTelemetryUseCase(
        device_repository=device_repo,
        telemetry_repository=None,
        uow=uow,
        outbox=outbox,
    )

    # -------------------------
    # WIRING CLEAN ARCH
    # -------------------------
    router = MQTTApplicationRouter(
        telemetry_uc=telemetry_uc,
        ack_uc=ack_uc,
    )

    translator = MQTTMessageTranslator()

    handler = MQTTHandler(
        translator=translator,
        router=router,
    )

    # -------------------------
    # EXECUTION (MQTT -> DOMAIN)
    # -------------------------
    result = handler.handle(
        topic="devices/dev1/ack",
        payload={"command_id": "cmd-1"},
        received_at=datetime.utcnow(),
    )

    # -------------------------
    # ASSERTIONS
    # -------------------------
    assert cmd.ack_called is True
    assert result is not None