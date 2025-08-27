"""
Use case: Start a new debate conversation.

Handles creation of new conversations when the user
sends the first message without conversation_id.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.application.exceptions import UseCaseException, ValidationException
from src.application.ports.conversation_repository import ConversationRepository
from src.domain import (
    Conversation,
    ConversationId, 
    DebateOrchestrator,
    MessageRole,
    PersonalityType,
)


@dataclass
class StartConversationRequest:
    """Request to start a new conversation."""
    
    message: str
    preferred_personality: Optional[PersonalityType] = None
    timestamp: Optional[datetime] = None


@dataclass 
class StartConversationResponse:
    """Response from conversation start."""
    
    conversation_id: str
    message: list[dict[str, str]]  # List of messages for API


class StartConversationUseCase:
    """
    Use case for starting new debate conversations.
    
    This use case:
    1. Validates user's initial message
    2. Creates a new conversation
    3. Adds user message
    4. Generates bot response using debate orchestrator
    5. Persists the conversation
    """
    
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        debate_orchestrator: DebateOrchestrator
    ):
        self._conversation_repository = conversation_repository
        self._debate_orchestrator = debate_orchestrator
    
    async def execute(self, request: StartConversationRequest) -> StartConversationResponse:
        """
        Execute the start conversation use case.
        
        Args:
            request: Data to start the conversation
            
        Returns:
            Response with the started conversation
            
        Raises:
            ValidationException: If input data is invalid
            UseCaseException: If there's an execution error
        """
        try:
            # Validar entrada
            self._validate_request(request)
            
            # Create new conversation
            conversation = self._create_new_conversation(request.timestamp)
            
            # Add user message
            user_message = conversation.add_user_message(
                content=request.message,
                timestamp=request.timestamp or datetime.now()
            )
            
            # Generar respuesta del bot
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
            
            # Persist conversation
            await self._conversation_repository.save(conversation)
            
            # Construir response
            return StartConversationResponse(
                conversation_id=str(conversation.id),
                message=conversation.get_messages_for_api()
            )
            
        except ValidationException:
            raise
        except Exception as e:
            raise UseCaseException(
                f"Failed to start conversation: {e}",
                "StartConversation"
            )
    
    def _validate_request(self, request: StartConversationRequest) -> None:
        """
        Validate input data.
        
        Args:
            request: Request to validate
            
        Raises:
            ValidationException: If data is invalid
        """
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
    
    def _create_new_conversation(self, timestamp: Optional[datetime] = None) -> Conversation:
        """
        Create a new conversation.
        
        Args:
            timestamp: Creation timestamp (optional)
            
        Returns:
            New created conversation
        """
        conversation_id = ConversationId.generate()
        created_at = timestamp or datetime.now()
        
        return Conversation(
            id=conversation_id,
            created_at=created_at
        )

