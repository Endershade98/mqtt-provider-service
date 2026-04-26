# src/application/use_cases/base.py
class UseCase:

    def __init__(self, outbox=None):
        self.outbox = outbox

    def commit(self, entity, repository):
        events = entity.pull_events()

        repository.save(entity)

        if self.outbox:
            self.outbox.save(events)

        return events