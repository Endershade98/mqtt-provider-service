# tests/unit/application/fakes/fake_outbox.py

class FakeOutbox:
    def __init__(self):
        self.saved_events = []

    def save(self, events):
        self.saved_events.extend(events)