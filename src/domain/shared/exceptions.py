# src/domain/shared/exceptions.py

# src/domain/shared/exceptions.py


class DomainError(Exception):
    """
    Base class for all domain-level exceptions.

    Raised when business rules, invariants,
    or domain validations are violated.
    """
    pass


# =====================================================
# STATE / BUSINESS RULES
# =====================================================

class InvalidStateTransition(DomainError):
    """
    Raised when an aggregate attempts
    an invalid lifecycle transition.
    """
    pass


# =====================================================
# VALUE OBJECT VALIDATION
# =====================================================

class InvalidDeviceId(DomainError):
    """
    Raised when DeviceId is empty or invalid.
    """
    pass


class InvalidCommandId(DomainError):
    """
    Raised when CommandId is empty or invalid.
    """
    pass


class InvalidTopicFormat(DomainError):
    """
    Raised when an MQTT topic
    does not match expected format.
    """
    pass


# =====================================================
# ENTITY VALIDATION
# =====================================================

class TelemetryValidationError(DomainError):
    """
    Raised when telemetry payload
    is missing or invalid.
    """
    pass


class CommandValidationError(DomainError):
    """
    Raised when command payload
    is invalid.
    """
    pass