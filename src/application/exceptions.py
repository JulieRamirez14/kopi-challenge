"""
Application layer exceptions.

Defines specific exceptions for use case errors.
"""


class ApplicationException(Exception):
    """Base exception for application layer errors."""
    
    def __init__(self, message: str, error_code: str = "APPLICATION_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class RepositoryException(ApplicationException):
    """Exception for repository errors."""
    
    def __init__(self, message: str):
        super().__init__(f"Repository error: {message}", "REPOSITORY_ERROR")


class UseCaseException(ApplicationException):
    """Exception for use case errors."""
    
    def __init__(self, message: str, use_case: str):
        super().__init__(f"Use case '{use_case}' failed: {message}", "USE_CASE_ERROR")
        self.use_case = use_case


class ValidationException(ApplicationException):
    """Exception for application layer validation errors."""
    
    def __init__(self, message: str):
        super().__init__(f"Validation error: {message}", "VALIDATION_ERROR")


class ConversationAlreadyExistsException(ApplicationException):
    """Exception for when trying to create a conversation that already exists."""
    
    def __init__(self, conversation_id: str):
        message = f"Conversation already exists: {conversation_id}"
        super().__init__(message, "CONVERSATION_ALREADY_EXISTS")
        self.conversation_id = conversation_id
