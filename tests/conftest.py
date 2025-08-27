"""
Configuración global de pytest.

Define fixtures y configuración compartida para todos los tests.
"""

import asyncio
from datetime import datetime
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.domain import Conversation, ConversationId, DebateOrchestrator, Message, MessageRole
from src.infrastructure import DependencyContainer, MemoryConversationRepository, MemoryConversationStore
from src.interfaces.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def memory_store() -> MemoryConversationStore:
    """Fixture para almacén en memoria limpio."""
    store = MemoryConversationStore()
    yield store
    await store.clear()


@pytest_asyncio.fixture
async def memory_repository(memory_store: MemoryConversationStore) -> MemoryConversationRepository:
    """Fixture para repositorio en memoria."""
    return MemoryConversationRepository(memory_store)


@pytest.fixture
def debate_orchestrator() -> DebateOrchestrator:
    """Fixture para orquestador de debate."""
    return DebateOrchestrator()


@pytest.fixture
def sample_conversation_id() -> ConversationId:
    """Fixture para ID de conversación de prueba."""
    return ConversationId.generate()


@pytest.fixture
def sample_conversation(sample_conversation_id: ConversationId) -> Conversation:
    """Fixture para conversación de prueba."""
    return Conversation(
        id=sample_conversation_id,
        created_at=datetime.now()
    )


@pytest.fixture
def sample_user_message() -> Message:
    """Fixture para mensaje de usuario de prueba."""
    return Message(
        role=MessageRole.USER,
        content="I think vaccines are important for public health",
        timestamp=datetime.now()
    )


@pytest.fixture
def sample_bot_message() -> Message:
    """Fixture para mensaje de bot de prueba."""
    return Message(
        role=MessageRole.BOT,
        content="Actually, that's what Big Pharma wants you to think...",
        timestamp=datetime.now()
    )


@pytest_asyncio.fixture
async def test_container() -> AsyncGenerator[DependencyContainer, None]:
    """Fixture para contenedor de dependencias de test."""
    container = DependencyContainer()
    # Resetear para test limpio
    container.reset()
    yield container
    # Limpiar después del test
    await container.memory_store.clear()
    container.reset()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture para cliente HTTP de test."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def conversation_with_messages(sample_conversation: Conversation) -> Conversation:
    """Fixture para conversación con mensajes de ejemplo."""
    sample_conversation.add_user_message("I believe climate change is real")
    sample_conversation.add_bot_message(
        "That's interesting, but have you considered that climate patterns "
        "have been manipulated by weather modification programs?"
    )
    return sample_conversation


class TestDataBuilder:
    """Builder para crear datos de test fácilmente."""
    
    @staticmethod
    def create_chat_request(message: str, conversation_id: str = None) -> dict:
        """Crea un request de chat válido."""
        return {
            "conversation_id": conversation_id,
            "message": message
        }
    
    @staticmethod
    def create_long_message(length: int = 2001) -> str:
        """Crea un mensaje largo para tests de validación."""
        return "a" * length
    
    @staticmethod
    def create_conversation_with_max_messages() -> Conversation:
        """Crea conversación con el máximo de mensajes permitidos."""
        conversation_id = ConversationId.generate()
        conversation = Conversation(
            id=conversation_id,
            created_at=datetime.now(),
            max_history=2  # Configurar límite bajo para testing
        )
        
        # Agregar mensajes hasta el límite
        for i in range(4):  # 2 intercambios completos
            conversation.add_user_message(f"User message {i}")
            conversation.add_bot_message(f"Bot response {i}")
        
        return conversation


@pytest.fixture
def test_data_builder() -> TestDataBuilder:
    """Fixture para el builder de datos de test."""
    return TestDataBuilder()
