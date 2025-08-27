"""
In-memory implementation of conversation repository.

This implementation fulfills the contract defined by ConversationRepository
using in-memory storage for simplicity and speed.
"""

from typing import Optional

from src.application.exceptions import RepositoryException
from src.application.ports import ConversationRepository
from src.domain import Conversation, ConversationId, ConversationNotFoundException
from src.infrastructure.exceptions import MemoryRepositoryException
from src.infrastructure.persistence.memory_store import MemoryConversationStore


class MemoryConversationRepository(ConversationRepository):
    """
    In-memory implementation of conversation repository.
    
    This implementation:
    - Uses MemoryConversationStore for thread-safe storage
    - Translates infrastructure exceptions to application exceptions
    - Provides complete CRUD operations for conversations
    """
    
    def __init__(self, memory_store: Optional[MemoryConversationStore] = None):
        """
        Initialize repository with memory store.
        
        Args:
            memory_store: Memory store (optional, creates one if not provided)
        """
        self._memory_store = memory_store or MemoryConversationStore()
    
    async def save(self, conversation: Conversation) -> None:
        """
        Save a conversation to the repository.
        
        Args:
            conversation: Conversation to save
            
        Raises:
            RepositoryException: If cannot save conversation
        """
        try:
            await self._memory_store.store(conversation)
        except MemoryRepositoryException as e:
            raise RepositoryException(f"Failed to save conversation: {e.message}")
        except Exception as e:
            raise RepositoryException(f"Unexpected error saving conversation: {e}")
    
    async def find_by_id(self, conversation_id: ConversationId) -> Optional[Conversation]:
        """
        Find a conversation by its ID.
        
        Args:
            conversation_id: ID of conversation to find
            
        Returns:
            Found conversation or None if doesn't exist
            
        Raises:
            RepositoryException: If there's an error in search
        """
        try:
            return await self._memory_store.retrieve(conversation_id)
        except MemoryRepositoryException as e:
            raise RepositoryException(f"Failed to find conversation: {e.message}")
        except Exception as e:
            raise RepositoryException(f"Unexpected error finding conversation: {e}")
    
    async def update(self, conversation: Conversation) -> None:
        """
        Update an existing conversation.
        
        Args:
            conversation: Conversation with updated data
            
        Raises:
            ConversationNotFoundException: If conversation doesn't exist
            RepositoryException: If there's an error in update
        """
        try:
            # Verify that conversation exists
            existing = await self._memory_store.retrieve(conversation.id)
            if not existing:
                raise ConversationNotFoundException(str(conversation.id))
            
            # Update
            await self._memory_store.update(conversation)
            
        except ConversationNotFoundException:
            raise
        except MemoryRepositoryException as e:
            # If memory store error indicates it doesn't exist, translate correctly
            if "not found" in e.message.lower():
                raise ConversationNotFoundException(str(conversation.id))
            else:
                raise RepositoryException(f"Failed to update conversation: {e.message}")
        except Exception as e:
            raise RepositoryException(f"Unexpected error updating conversation: {e}")
    
    async def delete(self, conversation_id: ConversationId) -> bool:
        """
        Delete a conversation from repository.
        
        Args:
            conversation_id: ID of conversation to delete
            
        Returns:
            True if deleted, False if didn't exist
            
        Raises:
            RepositoryException: If there's an error in deletion
        """
        try:
            return await self._memory_store.delete(conversation_id)
        except MemoryRepositoryException as e:
            raise RepositoryException(f"Failed to delete conversation: {e.message}")
        except Exception as e:
            raise RepositoryException(f"Unexpected error deleting conversation: {e}")
    
    async def count_active_conversations(self) -> int:
        """
        Count the number of active conversations.
        
        Returns:
            Number of conversations in repository
            
        Raises:
            RepositoryException: If there's an error in counting
        """
        try:
            return await self._memory_store.count()
        except MemoryRepositoryException as e:
            raise RepositoryException(f"Failed to count conversations: {e.message}")
        except Exception as e:
            raise RepositoryException(f"Unexpected error counting conversations: {e}")
    
    async def health_check(self) -> bool:
        """
        Check repository health.
        
        Returns:
            True if repository is working correctly
        """
        try:
            return await self._memory_store.health_check()
        except Exception:
            return False
    
    # Additional useful methods for debugging and administration
    
    async def get_all_conversation_ids(self) -> list[str]:
        """
        Get all conversation IDs (useful for debugging).
        
        Returns:
            List of conversation IDs
            
        Raises:
            RepositoryException: If there's an error getting IDs
        """
        try:
            return await self._memory_store.get_all_ids()
        except MemoryRepositoryException as e:
            raise RepositoryException(f"Failed to get conversation IDs: {e.message}")
        except Exception as e:
            raise RepositoryException(f"Unexpected error getting conversation IDs: {e}")
    
    async def clear_all_conversations(self) -> None:
        """
        Clear all conversations (useful for testing).
        
        ⚠️ WARNING: This operation is destructive.
        
        Raises:
            RepositoryException: If there's an error clearing
        """
        try:
            await self._memory_store.clear()
        except MemoryRepositoryException as e:
            raise RepositoryException(f"Failed to clear conversations: {e.message}")
        except Exception as e:
            raise RepositoryException(f"Unexpected error clearing conversations: {e}")
    
    def __str__(self) -> str:
        """String representation of repository."""
        return "MemoryConversationRepository"
    
    def __repr__(self) -> str:
        """Representation for debugging."""
        return f"MemoryConversationRepository(store={self._memory_store})"
