# tests/unit/application/test_outbox_usage.py

from unittest.mock import Mock
from src.application.use_cases.handle_telemetry import HandleTelemetryUseCase
from src.application.use_cases.dto.handle_telemetry_dto import HandleTelemetryDTO
from tests.unit.application.fakes.fake_unit_of_work import FakeUnitOfWork
from tests.unit.application.fakes.fake_outbox import FakeOutbox


def test_outbox_is_called():

    device_repo = Mock()
    telemetry_repo = Mock()

    outbox = FakeOutbox()
    uow = FakeUnitOfWork()

    device = Mock()
    device.pull_events.return_value = ["DeviceBecameOnline"]

    device_repo.get.return_value = device

    uc = HandleTelemetryUseCase(
        device_repo,
        telemetry_repo,
        uow,
        outbox
    )

    dto = HandleTelemetryDTO(
        device_id="dev-1",
        payload={"temp": 10},
        received_at=None
    )

    uc.execute(dto)

    assert len(outbox.saved_events) == 1