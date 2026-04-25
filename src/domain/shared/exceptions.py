# src/domain/shared/exceptions.py
class DomainError(Exception):
    pass


class InvalidStateTransition(DomainError):
    pass


class InvalidTopicFormat(DomainError):
    pass


class InvalidDeviceId(DomainError):
    pass