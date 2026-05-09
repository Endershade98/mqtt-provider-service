# src/infrastructure/persistence/django/unit_of_work.py

from django.db import transaction


class DjangoUnitOfWork:
    """
    Concrete Unit of Work for Django ORM.

    Responsibilities:
    - open atomic transaction
    - commit on success
    - rollback on exception
    """

    def __enter__(self):
        self._ctx = transaction.atomic()
        self._ctx.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._ctx.__exit__(exc_type, exc_val, exc_tb)

    def commit(self):
        """
        Optional explicit commit hook.
        Django atomic commits automatically on exit if no exception.
        """
        return None

    def rollback(self):
        """
        Optional rollback hook.
        Real rollback handled by atomic on exception.
        """
        pass