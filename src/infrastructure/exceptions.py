"""
Infrastructure layer exceptions.

Defines specific exceptions for errors in concrete implementations.
"""


class InfrastructureException(Exception):
    """Base exception for infrastructure errors."""
    
    def __init__(self, message: str, error_code: str = "INFRASTRUCTURE_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class PersistenceException(InfrastructureException):
    """Exception for persistence errors."""
    
    def __init__(self, message: str):
        super().__init__(f"Persistence error: {message}", "PERSISTENCE_ERROR")


class MemoryRepositoryException(PersistenceException):
    """Specific exception for memory repository."""
    
    def __init__(self, message: str, operation: str):
        super().__init__(f"Memory repository operation '{operation}' failed: {message}")
        self.operation = operation


class AdapterException(InfrastructureException):
    """Exception for external adapter errors."""
    
    def __init__(self, message: str, adapter: str):
        super().__init__(f"Adapter '{adapter}' error: {message}", "ADAPTER_ERROR")
        self.adapter = adapter
