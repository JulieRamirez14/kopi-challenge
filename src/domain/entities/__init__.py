# Domain Entities - Core business objects

from .conversation import Conversation
from .message import Message, MessageRole

__all__ = [
    "Conversation",
    "Message", 
    "MessageRole",
]