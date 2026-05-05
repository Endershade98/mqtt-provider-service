
# src/application/use_cases/base.py

from src.application.ports.outbox import OutboxPort
from src.application.ports.unit_of_work import UnitOfWork


class UseCase:
    """
    Base application use case.

    Responsibilities:
    - transaction boundary
    - persist aggregate
    - persist emitted domain events
    """

    def __init__(self, uow: UnitOfWork, outbox: OutboxPort):
        self.uow = uow
        self.outbox = outbox

    def commit(self, entity, repository):
        events = entity.pull_events()

        repository.save(entity)
        self.outbox.save(events)

        return events