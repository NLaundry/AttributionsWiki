"""Exceptions for the application."""

class ValidationError(Exception):
    """Exception raised for validation errors."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(f"Validation error: {message}", *args)


class DatabaseError(Exception):
    """Exception raised when a database operation fails."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(f"Database error: {message}", *args)


class NotFoundError(Exception):
    """Exception raised when an item is not found."""

    pass


class UpdateError(Exception):
    """Exception raised when an update operation fails."""

    pass


class DeletionError(Exception):
    """Exception raised when a deletion operation fails."""

    pass
