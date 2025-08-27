"""
Domain exceptions.

Defines domain-specific exceptions for handling business errors.
"""


class DomainException(Exception):
    """Base exception for domain errors."""
    
    def __init__(self, message: str, error_code: str = "DOMAIN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class ConversationNotFoundException(DomainException):
    """Exception for when a conversation is not found."""
    
    def __init__(self, conversation_id: str):
        message = f"Conversation not found: {conversation_id}"
        super().__init__(message, "CONVERSATION_NOT_FOUND")
        self.conversation_id = conversation_id


class InvalidMessageException(DomainException):
    """Exception for invalid messages."""
    
    def __init__(self, message: str):
        super().__init__(f"Invalid message: {message}", "INVALID_MESSAGE")


class ConversationLimitExceededException(DomainException):
    """Exception for when message limit is exceeded."""
    
    def __init__(self, limit: int):
        message = f"Conversation limit exceeded: {limit} messages"
        super().__init__(message, "CONVERSATION_LIMIT_EXCEEDED")
        self.limit = limit


class DebateGenerationException(DomainException):
    """Exception for errors in debate response generation."""
    
    def __init__(self, message: str):
        super().__init__(f"Debate generation failed: {message}", "DEBATE_GENERATION_FAILED")

