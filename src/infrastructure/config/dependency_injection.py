"""
Dependency Injection configuration.

Configures and injects all system dependencies using the
dependency injection pattern to maintain low coupling.
"""

from functools import lru_cache
from typing import Optional

from src.application.ports.conversation_repository import ConversationRepository
from src.application.use_cases.continue_debate import ContinueDebateUseCase
from src.application.use_cases.start_conversation import StartConversationUseCase
from src.domain.services.debate_orchestrator import DebateOrchestrator
from src.infrastructure.persistence.memory_store import MemoryConversationStore
from src.infrastructure.repositories.memory_conversation_repository import MemoryConversationRepository


class DependencyContainer:
    """
    Dependency container for the application.
    
    Centralizes creation and configuration of all dependencies,
    implementing Singleton pattern to ensure unique instances.
    """
    
    _instance: Optional['DependencyContainer'] = None
    
    def __new__(cls) -> 'DependencyContainer':
        """Implements Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize container (only once due to Singleton)."""
        if not hasattr(self, '_initialized'):
            self._memory_store: Optional[MemoryConversationStore] = None
            self._conversation_repository: Optional[ConversationRepository] = None
            self._debate_orchestrator: Optional[DebateOrchestrator] = None
            self._start_conversation_use_case: Optional[StartConversationUseCase] = None
            self._continue_debate_use_case: Optional[ContinueDebateUseCase] = None
            self._initialized = True
    
    @property
    @lru_cache(maxsize=1)
    def memory_store(self) -> MemoryConversationStore:
        """
        Get singleton instance of memory store.
        
        Returns:
            Unique instance of MemoryConversationStore
        """
        if self._memory_store is None:
            self._memory_store = MemoryConversationStore()
        return self._memory_store
    
    @property
    @lru_cache(maxsize=1)
    def conversation_repository(self) -> ConversationRepository:
        """
        Get singleton instance of conversation repository.
        
        Returns:
            Unique instance implementing ConversationRepository
        """
        if self._conversation_repository is None:
            self._conversation_repository = MemoryConversationRepository(
                memory_store=self.memory_store
            )
        return self._conversation_repository
    
    @property
    @lru_cache(maxsize=1) 
    def debate_orchestrator(self) -> DebateOrchestrator:
        """
        Get singleton instance of debate orchestrator.
        
        Returns:
            Unique instance of DebateOrchestrator
        """
        if self._debate_orchestrator is None:
            self._debate_orchestrator = DebateOrchestrator()
        return self._debate_orchestrator
    
    @property
    @lru_cache(maxsize=1)
    def start_conversation_use_case(self) -> StartConversationUseCase:
        """
        Get instance of use case for starting conversations.
        
        Returns:
            Configured instance of StartConversationUseCase
        """
        if self._start_conversation_use_case is None:
            self._start_conversation_use_case = StartConversationUseCase(
                conversation_repository=self.conversation_repository,
                debate_orchestrator=self.debate_orchestrator
            )
        return self._start_conversation_use_case
    
    @property
    @lru_cache(maxsize=1)
    def continue_debate_use_case(self) -> ContinueDebateUseCase:
        """
        Get instance of use case for continuing debates.
        
        Returns:
            Configured instance of ContinueDebateUseCase
        """
        if self._continue_debate_use_case is None:
            self._continue_debate_use_case = ContinueDebateUseCase(
                conversation_repository=self.conversation_repository,
                debate_orchestrator=self.debate_orchestrator
            )
        return self._continue_debate_use_case
    
    def health_check(self) -> dict[str, bool]:
        """
        Check health of all components.
        
        Returns:
            Dictionary with health status of each component
        """
        return {
            "memory_store": True,
            "conversation_repository": True,
            "debate_orchestrator": True,
        }
    
    def reset(self) -> None:
        """
        Reset the container (useful for testing).
        
        ⚠️ WARNING: This will delete all cached instances.
        """
        self._memory_store = None
        self._conversation_repository = None
        self._debate_orchestrator = None
        self._start_conversation_use_case = None
        self._continue_debate_use_case = None
        
        # Clear lru_cache cache
        self.memory_store.fget.cache_clear()
        self.conversation_repository.fget.cache_clear()
        self.debate_orchestrator.fget.cache_clear()
        self.start_conversation_use_case.fget.cache_clear()
        self.continue_debate_use_case.fget.cache_clear()


# Global container instance (Singleton)
container = DependencyContainer()


def get_container() -> DependencyContainer:
    """
    Convenience function to get dependency container.
    
    Returns:
        Unique instance of dependency container
    """
    return container


def get_start_conversation_use_case() -> StartConversationUseCase:
    """Get use case for starting conversations."""
    return container.start_conversation_use_case


def get_continue_debate_use_case() -> ContinueDebateUseCase:
    """Get use case for continuing debates."""
    return container.continue_debate_use_case
