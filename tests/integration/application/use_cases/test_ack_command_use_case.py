# tests/unit/application/use_cases/test_ack_command_use_case.py

import pytest

from src.application.use_cases.ack_command import AcknowledgeCommandUseCase
from src.application.use_cases.dto.ack_command_dto import AckCommandDTO
from src.application.exceptions import CommandNotFoundError

from src.domain.command.entity import Command
from src.domain.command.value_objects import CommandId, CommandStatus
from src.domain.device.value_objects import DeviceId

from tests.unit.application.fakes.fake_command_repository import (
    FakeCommandRepository,
)
from tests.unit.application.fakes.fake_unit_of_work import (
    FakeUnitOfWork,
)
from tests.unit.application.fakes.fake_outbox import (
    FakeOutbox,
)


# =====================================================
# HELPERS
# =====================================================

def make_sent_command(
    command_id: str = "cmd-1",
    device_id: str = "dev-1",
):
    """
    Creates a command already in SENT state.
    Required because only SENT -> ACKED is valid.
    """
    command = Command.create(
        command_id=CommandId(command_id),
        device_id=DeviceId(device_id),
        payload={"action": "ping"},
    )

    command.send()

    # clear previous events (Created + Sent)
    command.pull_events()

    return command


def make_use_case(repo=None, uow=None, outbox=None):
    repo = repo or FakeCommandRepository()
    uow = uow or FakeUnitOfWork()
    outbox = outbox or FakeOutbox()

    use_case = AcknowledgeCommandUseCase(
        command_repository=repo,
        uow=uow,
        outbox=outbox,
    )

    return use_case, repo, uow, outbox


# =====================================================
# TESTS
# =====================================================

def test_ack_command_success():
    use_case, repo, uow, outbox = make_use_case()

    command = make_sent_command("cmd-1")
    repo.save(command)

    dto = AckCommandDTO(command_id="cmd-1")

    result = use_case.execute(dto)

    assert result.status == CommandStatus.ACKED


def test_ack_command_persists_updated_command():
    use_case, repo, uow, outbox = make_use_case()

    command = make_sent_command("cmd-2")
    repo.save(command)

    use_case.execute(
        AckCommandDTO(command_id="cmd-2")
    )

    saved = repo.get(CommandId("cmd-2"))

    assert saved.status == CommandStatus.ACKED


def test_ack_command_commits_unit_of_work():
    use_case, repo, uow, outbox = make_use_case()

    command = make_sent_command("cmd-3")
    repo.save(command)

    use_case.execute(
        AckCommandDTO(command_id="cmd-3")
    )

    assert uow.committed is True


def test_ack_command_saves_outbox_event():
    use_case, repo, uow, outbox = make_use_case()

    command = make_sent_command("cmd-4")
    repo.save(command)

    use_case.execute(
        AckCommandDTO(command_id="cmd-4")
    )

    assert len(outbox.saved_events) == 1
    assert (
        outbox.saved_events[0].__class__.__name__
        == "CommandAcknowledged"
    )


def test_ack_command_event_contains_command_id():
    use_case, repo, uow, outbox = make_use_case()

    command = make_sent_command("cmd-5")
    repo.save(command)

    use_case.execute(
        AckCommandDTO(command_id="cmd-5")
    )

    event = outbox.saved_events[0]

    assert event.command_id == "cmd-5"


def test_ack_command_not_found_raises_error():
    use_case, repo, uow, outbox = make_use_case()

    dto = AckCommandDTO(command_id="missing")

    with pytest.raises(CommandNotFoundError):
        use_case.execute(dto)


def test_ack_command_returns_same_updated_aggregate():
    use_case, repo, uow, outbox = make_use_case()

    command = make_sent_command("cmd-6")
    repo.save(command)

    result = use_case.execute(
        AckCommandDTO(command_id="cmd-6")
    )

    assert result.command_id.value == "cmd-6"
    assert result.status == CommandStatus.ACKED


def test_ack_command_consumes_domain_events_after_commit():
    use_case, repo, uow, outbox = make_use_case()

    command = make_sent_command("cmd-7")
    repo.save(command)

    result = use_case.execute(
        AckCommandDTO(command_id="cmd-7")
    )

    # events already flushed to outbox
    assert result.pull_events() == []