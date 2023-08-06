"""Custom exceptions."""


class MalformedSnsPayloadError(Exception):
    """Error raised when the event payload is not a valid event."""


class EnvironmentVariableNotFound(Exception):
    """Error raised when the environment variables are not set."""
