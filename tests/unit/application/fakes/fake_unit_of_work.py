# tests/unit/application/fakes/fake_unit_of_work.py

class FakeUnitOfWork:
    def __init__(self):
        self.committed = False
        self.entered = False
        self.exited = False

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(self, exc_type, exc, tb):
        self.exited = True

    def commit(self):
        self.committed = True

    def rollback(self):
        pass