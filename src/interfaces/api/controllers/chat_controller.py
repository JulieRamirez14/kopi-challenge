"""
Controlador para el API de chat.

Maneja las requests HTTP y coordina con los casos de uso de la aplicación.
"""

from datetime import datetime
from typing import Dict, Any

import logging
from fastapi import HTTPException, status

from src.application.exceptions import (
    ApplicationException,
    RepositoryException,
    UseCaseException,
    ValidationException,
)
from src.application.use_cases import (
    ContinueDebateRequest,
    ContinueDebateUseCase,
    StartConversationRequest, 
    StartConversationUseCase,
)
from src.interfaces.api.schemas.chat_schemas import ChatRequest, ChatResponse
from src.infrastructure.config.dependency_injection import (
    get_start_conversation_use_case,
    get_continue_debate_use_case
)

logger = logging.getLogger(__name__)


class ChatController:
    """
    Controlador REST para operaciones de chat.
    
    Maneja las requests HTTP y coordina con los casos de uso,
    traduciendo entre el protocolo HTTP y la lógica de aplicación.
    """
    
    def __init__(self):
        """Inicializa el controlador con las dependencias."""
        pass
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Endpoint principal de chat que maneja tanto conversaciones nuevas como existentes.
        
        Args:
            request: Request validado con los datos de chat
            
        Returns:
            Response con la conversación actualizada
            
        Raises:
            HTTPException: Para errores HTTP específicos
        """
        try:
            logger.info(f"Processing chat request: conversation_id={request.conversation_id}, message_length={len(request.message)}")
            
            # Determine if it's new or existing conversation
            if request.conversation_id is None:
                # New conversation
                response = await self._start_new_conversation(request)
                logger.info(f"Started new conversation: {response.conversation_id}, messages: {len(response.message)}")
            else:
                # Continue existing conversation
                response = await self._continue_existing_conversation(request)
                logger.info(f"Continued existing conversation: {response.conversation_id}, messages: {len(response.message)}")
            
            return response
            
        except ValidationException as e:
            logger.warning(f"Validation error in chat: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "VALIDATION_ERROR",
                    "message": str(e),
                    "details": "Please check your input data"
                }
            )
        
        except Exception as app_e:
            logger.warning(f"Application error: {app_e}")
            # Specific handling of conversation not found
            if "ConversationNotFoundException" in str(type(app_e)) or "not found" in str(app_e).lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error": "CONVERSATION_NOT_FOUND", "message": str(app_e)}
                )
            else:
                # Para simplicidad, otros errores como 500
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={"error": "INTERNAL_ERROR", "message": "Internal server error"}
                )
        
        except Exception as e:
            logger.error(f"Unexpected error in chat: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "UNEXPECTED_ERROR",
                    "message": "An unexpected error occurred",
                    "details": "Please try again later or contact support"
                }
            )
    
    async def _start_new_conversation(self, request: ChatRequest) -> ChatResponse:
        """
        Inicia una nueva conversación.
        
        Args:
            request: Request de chat
            
        Returns:
            Response con la nueva conversación
        """
        use_case = get_start_conversation_use_case()
        
        # Crear request del caso de uso
        use_case_request = StartConversationRequest(
            message=request.message,
            timestamp=datetime.now()
        )
        
        # Ejecutar caso de uso
        use_case_response = await use_case.execute(use_case_request)
        
        # Convertir a response del API
        return ChatResponse(
            conversation_id=use_case_response.conversation_id,
            message=[
                {
                    "role": msg["role"],
                    "message": msg["message"]
                }
                for msg in use_case_response.message
            ]
        )
    
    async def _continue_existing_conversation(self, request: ChatRequest) -> ChatResponse:
        """
        Continúa una conversación existente.
        
        Args:
            request: Request de chat con conversation_id
            
        Returns:
            Response con la conversación actualizada
        """
        use_case = get_continue_debate_use_case()
        
        # Crear request del caso de uso
        use_case_request = ContinueDebateRequest(
            conversation_id=request.conversation_id,  # Ya validado por Pydantic
            message=request.message,
            timestamp=datetime.now()
        )
        
        # Ejecutar caso de uso
        use_case_response = await use_case.execute(use_case_request)
        
        # Convertir a response del API
        return ChatResponse(
            conversation_id=use_case_response.conversation_id,
            message=[
                {
                    "role": msg["role"],
                    "message": msg["message"]
                }
                for msg in use_case_response.message
            ]
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """Basic health check."""
        return {
            "status": "healthy",
            "components": {"api": True, "memory": True, "orchestrator": True},
            "timestamp": datetime.now().isoformat()
        }
