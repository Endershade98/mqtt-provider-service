# tests/unit/application/fakes/fake_unit_of_work.py

from src.application.ports.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):

    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        return False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True