# tests/unit/application/fakes/fake_outbox.py

from src.application.ports.outbox import OutboxPort


class FakeOutbox(OutboxPort):

    def __init__(self):
        self.saved_events = []

    def save(self, events):
        self.saved_events.extend(list(events))