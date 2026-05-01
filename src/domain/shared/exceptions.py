# src/domain/shared/exceptions.py
class DomainError(Exception):
    """Base class for all domain-related exceptions."""
    pass


class InvalidStateTransition(DomainError):
    """Raised when an entity attempts to transition to an invalid state."""
    pass


class InvalidTopicFormat(DomainError):
    """Raised when a topic string does not conform to the expected format."""
    pass


class InvalidDeviceId(DomainError):
    """Raised when a provided device ID is invalid, such as being empty or containing invalid characters."""
    pass


class TelemetryValidationError(DomainError):
    """Raised when telemetry data fails validation checks, such as missing required fields or invalid values."""
    pass


class CommandValidationError(DomainError):
    """Raised when a command fails validation checks, such as missing required fields or invalid values."""
    pass

class InvalidCommandId(DomainError):
    """Raised when a provided command ID is invalid, such as being empty or containing invalid characters."""
    pass

class DeviceNotFound(DomainError):
    """Raised when a device with the specified ID is not found."""
    pass

class CommandNotFound(DomainError):
    """Raised when a command with the specified ID is not found."""
    pass