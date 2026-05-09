# src/application/exceptions.py


class ApplicationError(Exception):
    """
    Base class for all application layer exceptions.

    Raised by use cases during orchestration,
    resource loading, unsupported operations,
    or workflow failures.
    """
    pass


# =====================================================
# RESOURCE LOOKUP FAILURES
# =====================================================

class ResourceNotFound(ApplicationError):
    """
    Generic requested resource not found.
    """
    pass


class DeviceNotFoundError(ResourceNotFound):
    def __init__(self, device_id: str):
        super().__init__(f"Device '{device_id}' not found")


class CommandNotFoundError(ResourceNotFound):
    def __init__(self, command_id: str):
        super().__init__(f"Command '{command_id}' not found")


# =====================================================
# APPLICATION FLOW ERRORS
# =====================================================

class UnsupportedOperationError(ApplicationError):
    """
    Raised when a requested application
    operation is unsupported.
    """
    pass


class UnsupportedDeviceStateTransitionError(
    UnsupportedOperationError
):
    def __init__(self, target_status):
        super().__init__(
            f"Unsupported target status '{target_status}'"
        )