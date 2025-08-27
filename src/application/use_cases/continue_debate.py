"""
Use case: Continue an existing debate.

Handles continuation of conversations when the user
sends a message with an existing conversation_id.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.application.exceptions import UseCaseException, ValidationException
from src.application.ports.conversation_repository import ConversationRepository
from src.domain import (
    ConversationId,
    ConversationNotFoundException,
    DebateOrchestrator,
    PersonalityType,
)


@dataclass
class ContinueDebateRequest:
    """Request to continue an existing debate."""
    
    conversation_id: str
    message: str
    preferred_personality: Optional[PersonalityType] = None
    timestamp: Optional[datetime] = None


@dataclass
class ContinueDebateResponse:
    """Response from debate continuation."""
    
    conversation_id: str
    message: list[dict[str, str]]  # List of messages for API


class ContinueDebateUseCase:
    """
    Use case for continuing existing debates.
    
    This use case:
    1. Validates message and conversation_id
    2. Retrieves existing conversation
    3. Adds new user message
    4. Generates bot response maintaining context
    5. Updates conversation in repository
    """
    
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        debate_orchestrator: DebateOrchestrator
    ):
        self._conversation_repository = conversation_repository
        self._debate_orchestrator = debate_orchestrator
    
    async def execute(self, request: ContinueDebateRequest) -> ContinueDebateResponse:
        """
        Execute the continue debate use case.
        
        Args:
            request: Data to continue the debate
            
        Returns:
            Response with updated conversation
            
        Raises:
            ValidationException: If input data is invalid
            ConversationNotFoundException: If conversation doesn't exist
            UseCaseException: If there's an execution error
        """
        try:
            # Validar entrada
            self._validate_request(request)
            
            # Convertir conversation_id string a ConversationId
            conversation_id = ConversationId.from_string(request.conversation_id)
            
            # Retrieve existing conversation
            conversation = await self._conversation_repository.find_by_id(conversation_id)
            if not conversation:
                raise ConversationNotFoundException(request.conversation_id)
            
            # Add user message
            user_message = conversation.add_user_message(
                content=request.message,
                timestamp=request.timestamp or datetime.now()
            )
            
            # Generar respuesta del bot usando contexto existente
            bot_response = self._debate_orchestrator.generate_bot_response(
                conversation=conversation,
                user_message=user_message,
                preferred_personality=request.preferred_personality
            )
            
            # Add bot response
            conversation.add_bot_message(
                content=bot_response,
                timestamp=datetime.now()
            )
            
            # Update conversation in repository
            await self._conversation_repository.update(conversation)
            
            # Construir response
            return ContinueDebateResponse(
                conversation_id=str(conversation.id),
                message=conversation.get_messages_for_api()
            )
            
        except (ValidationException, ConversationNotFoundException):
            raise
        except Exception as e:
            raise UseCaseException(
                f"Failed to continue debate: {e}",
                "ContinueDebate"
            )
    
    def _validate_request(self, request: ContinueDebateRequest) -> None:
        """
        Validate input data.
        
        Args:
            request: Request to validate
            
        Raises:
            ValidationException: If data is invalid
        """
        # Validar conversation_id
        if not request.conversation_id or not request.conversation_id.strip():
            raise ValidationException("Conversation ID cannot be empty")
        
        # Validar que conversation_id tenga formato UUID
        try:
            ConversationId.from_string(request.conversation_id)
        except ValueError as e:
            raise ValidationException(f"Invalid conversation ID format: {e}")
        
        # Validar mensaje
        if not request.message or not request.message.strip():
            raise ValidationException("Message cannot be empty")
        
        if len(request.message.strip()) > 2000:
            raise ValidationException("Message too long (max 2000 characters)")
        
        if len(request.message.strip()) < 5:
            raise ValidationException("Message too short (min 5 characters)")
        
        # Validar personalidad si se especifica
        if request.preferred_personality:
            available_personalities = self._debate_orchestrator.get_available_personalities()
            if request.preferred_personality not in available_personalities:
                raise ValidationException(
                    f"Invalid personality: {request.preferred_personality}. "
                    f"Available: {[p.value for p in available_personalities]}"
                )
    
    async def get_conversation_stats(self, conversation_id: str) -> dict[str, any]:
        """
        Get statistics from a specific conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Dictionary with debate statistics
            
        Raises:
            ConversationNotFoundException: If conversation doesn't exist
            UseCaseException: If there's an error getting statistics
        """
        try:
            # Validar y convertir conversation_id
            conv_id = ConversationId.from_string(conversation_id)
            
            # Retrieve conversation
            conversation = await self._conversation_repository.find_by_id(conv_id)
            if not conversation:
                raise ConversationNotFoundException(conversation_id)
            
            # Get statistics using orchestrator
            return self._debate_orchestrator.get_debate_statistics(conversation)
            
        except ConversationNotFoundException:
            raise
        except Exception as e:
            raise UseCaseException(
                f"Failed to get conversation stats: {e}",
                "GetConversationStats"
            )
