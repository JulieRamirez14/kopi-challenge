"""
Tests unitarios para los casos de uso de la aplicación.

Valida la lógica de negocio de los casos de uso principales.
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, Mock

from src.application.exceptions import ValidationException
from src.application.use_cases import (
    ContinueDebateRequest,
    ContinueDebateUseCase,
    StartConversationRequest,
    StartConversationUseCase,
)
from src.domain import (
    Conversation,
    ConversationId,
    ConversationNotFoundException,
    DebateOrchestrator,
    MessageRole,
)


class TestStartConversationUseCase:
    """Tests para el caso de uso StartConversation."""
    
    @pytest.fixture
    def mock_repository(self):
        """Mock del repositorio de conversaciones."""
        mock = Mock()
        mock.save = AsyncMock()
        mock.update = AsyncMock()
        mock.find_by_id = AsyncMock()
        return mock
    
    @pytest.fixture
    def mock_orchestrator(self):
        """Mock del orquestador de debate."""
        mock = Mock(spec=DebateOrchestrator)
        mock.generate_bot_response.return_value = "This is a bot response!"
        return mock
    
    @pytest.fixture
    def use_case(self, mock_repository, mock_orchestrator):
        """Fixture del caso de uso con mocks."""
        return StartConversationUseCase(
            conversation_repository=mock_repository,
            debate_orchestrator=mock_orchestrator
        )
    
    @pytest.mark.asyncio
    async def test_start_conversation_success(self, use_case, mock_repository, mock_orchestrator):
        """Test exitoso de iniciar conversación."""
        # Arrange
        request = StartConversationRequest(
            message="I think vaccines are important",
            timestamp=datetime.now()
        )
        
        # Act
        response = await use_case.execute(request)
        
        # Assert
        assert response.conversation_id is not None
        assert len(response.messages) == 2  # User + Bot message
        assert response.messages[0]["role"] == "user"
        assert response.messages[0]["message"] == "I think vaccines are important"
        assert response.messages[1]["role"] == "bot"
        assert response.messages[1]["message"] == "This is a bot response!"
        
        # Verify repository was called
        mock_repository.save.assert_called_once()
        
        # Verify orchestrator was called
        mock_orchestrator.generate_bot_response.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_start_conversation_empty_message_fails(self, use_case):
        """Test que mensaje vacío falla validación."""
        request = StartConversationRequest(message="")
        
        with pytest.raises(ValidationException, match="cannot be empty"):
            await use_case.execute(request)
    
    @pytest.mark.asyncio
    async def test_start_conversation_short_message_fails(self, use_case):
        """Test que mensaje muy corto falla validación."""
        request = StartConversationRequest(message="Hi")
        
        with pytest.raises(ValidationException, match="too short"):
            await use_case.execute(request)
    
    @pytest.mark.asyncio
    async def test_start_conversation_long_message_fails(self, use_case):
        """Test que mensaje muy largo falla validación."""
        long_message = "a" * 2001
        request = StartConversationRequest(message=long_message)
        
        with pytest.raises(ValidationException, match="too long"):
            await use_case.execute(request)


class TestContinueDebateUseCase:
    """Tests para el caso de uso ContinueDebate."""
    
    @pytest.fixture
    def mock_repository(self):
        """Mock del repositorio de conversaciones."""
        mock = Mock()
        mock.save = AsyncMock()
        mock.update = AsyncMock() 
        mock.find_by_id = AsyncMock()
        
        # Setup para que retorne la conversación con el ID correcto
        def mock_find_by_id(conversation_id):
            existing_conversation = Conversation(
                id=conversation_id,  # Usar el ID que se pasa como parámetro
                created_at=datetime.now()
            )
            existing_conversation.add_user_message("Previous message")
            existing_conversation.add_bot_message("Previous response")
            return existing_conversation
        
        mock.find_by_id.side_effect = mock_find_by_id
        return mock
    
    @pytest.fixture
    def mock_orchestrator(self):
        """Mock del orquestador de debate."""
        mock = Mock(spec=DebateOrchestrator)
        mock.generate_bot_response.return_value = "Continued bot response!"
        return mock
    
    @pytest.fixture
    def use_case(self, mock_repository, mock_orchestrator):
        """Fixture del caso de uso con mocks."""
        return ContinueDebateUseCase(
            conversation_repository=mock_repository,
            debate_orchestrator=mock_orchestrator
        )
    
    @pytest.mark.asyncio
    async def test_continue_debate_success(self, use_case, mock_repository, mock_orchestrator):
        """Test exitoso de continuar debate."""
        # Arrange
        conversation_id = str(ConversationId.generate())
        request = ContinueDebateRequest(
            conversation_id=conversation_id,
            message="I still disagree with you",
            timestamp=datetime.now()
        )
        
        # Act
        response = await use_case.execute(request)
        
        # Assert
        assert response.conversation_id == conversation_id
        assert len(response.messages) >= 2  # Al menos user + bot
        
        # Verify repository calls
        mock_repository.find_by_id.assert_called_once()
        mock_repository.update.assert_called_once()
        
        # Verify orchestrator was called
        mock_orchestrator.generate_bot_response.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_continue_debate_conversation_not_found(self, use_case, mock_repository):
        """Test error cuando conversación no existe."""
        # Arrange
        # Configurar el mock para retornar None (sobrescribiendo el side_effect)
        mock_repository.find_by_id.return_value = None
        mock_repository.find_by_id.side_effect = None
        
        conversation_id = str(ConversationId.generate())
        request = ContinueDebateRequest(
            conversation_id=conversation_id,
            message="Some message"
        )
        
        # Act & Assert
        with pytest.raises(ConversationNotFoundException):
            await use_case.execute(request)
    
    @pytest.mark.asyncio
    async def test_continue_debate_invalid_conversation_id(self, use_case):
        """Test error con ID de conversación inválido."""
        request = ContinueDebateRequest(
            conversation_id="invalid-uuid",
            message="Some message"
        )
        
        with pytest.raises(ValidationException, match="Invalid conversation ID format"):
            await use_case.execute(request)
    
    @pytest.mark.asyncio
    async def test_continue_debate_empty_conversation_id(self, use_case):
        """Test error con ID de conversación vacío."""
        request = ContinueDebateRequest(
            conversation_id="",
            message="Some message"
        )
        
        with pytest.raises(ValidationException, match="cannot be empty"):
            await use_case.execute(request)
    
    @pytest.mark.asyncio
    async def test_continue_debate_empty_message(self, use_case):
        """Test error con mensaje vacío."""
        conversation_id = str(ConversationId.generate())
        request = ContinueDebateRequest(
            conversation_id=conversation_id,
            message=""
        )
        
        with pytest.raises(ValidationException, match="cannot be empty"):
            await use_case.execute(request)
