"""
Esquemas Pydantic para la API de chat.

Define los modelos de datos de entrada y salida para el API REST,
siguiendo exactamente las especificaciones del challenge.
"""

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class MessageSchema(BaseModel):
    """Esquema para un mensaje individual en la respuesta."""
    
    role: str = Field(..., description="Rol del mensaje: 'user' o 'bot'")
    message: str = Field(..., description="Contenido del mensaje")
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate that role is valid."""
        if v not in ['user', 'bot']:
            raise ValueError("Role must be 'user' or 'bot'")
        return v
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Validate that message is not empty."""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class ChatRequest(BaseModel):
    """
    Esquema de request para el endpoint de chat.
    
    Sigue exactamente el formato especificado en el challenge:
    {
        "conversation_id": "text" | null,
        "message": "text"
    }
    """
    
    conversation_id: Optional[str] = Field(
        None, 
        description="ID de conversación existente, null para nueva conversación"
    )
    message: str = Field(
        ..., 
        min_length=1,
        max_length=2000,
        description="Mensaje del usuario"
    )
    
    @field_validator('message')
    @classmethod
    def validate_message_content(cls, v: str) -> str:
        """Valida y limpia el contenido del mensaje."""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        
        cleaned = v.strip()
        if len(cleaned) < 5:
            raise ValueError("Message too short (minimum 5 characters)")
        
        return cleaned
    
    @field_validator('conversation_id')
    @classmethod
    def validate_conversation_id(cls, v: Optional[str]) -> Optional[str]:
        """Valida el formato del conversation_id si se proporciona."""
        if v is None:
            return v
        
        if not v.strip():
            raise ValueError("Conversation ID cannot be empty string")
        
        # Validar formato UUID básico (sin importar uuid para mejor performance)
        cleaned = v.strip()
        if len(cleaned) != 36 or cleaned.count('-') != 4:
            raise ValueError("Conversation ID must be a valid UUID format")
        
        return cleaned


class ChatResponse(BaseModel):
    """
    Esquema de response para el endpoint de chat.
    
    Sigue exactamente el formato especificado en el challenge:
    {
        "conversation_id": "text",
        "messages": [
            {
                "role": "user",
                "message": "text"
            },
            {
                "role": "bot",
                "message": "text"
            }
        ]
    }
    """
    
    conversation_id: str = Field(
        ..., 
        description="ID único de la conversación"
    )
    message: List[MessageSchema] = Field(
        ..., 
        description="History of the 5 most recent exchanges"
    )
    
    @field_validator('message')
    @classmethod
    def validate_messages_count(cls, v: List[MessageSchema]) -> List[MessageSchema]:
        """Validate that message limits are not exceeded."""
        if len(v) > 10:  # Máximo 5 intercambios = 10 mensajes
            raise ValueError("Too many messages in response")
        
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "message": [
                    {
                        "role": "user",
                        "message": "I think vaccines are important for public health"
                    },
                    {
                        "role": "bot", 
                        "message": "Actually, that's exactly what Big Pharma wants you to think. Have you considered that natural immunity is far superior? Studies show that countries with lower vaccination rates have stronger populations..."
                    }
                ]
            }
        }
    }


class ErrorResponse(BaseModel):
    """Esquema para respuestas de error."""
    
    error: str = Field(..., description="Código de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    details: Optional[str] = Field(None, description="Detalles adicionales del error")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": "Message cannot be empty"
            }
        }
    }


class HealthResponse(BaseModel):
    """Esquema para el endpoint de health check."""
    
    status: str = Field(..., description="Estado general del servicio")
    components: dict = Field(..., description="Estado de componentes individuales")
    timestamp: str = Field(..., description="Timestamp del health check")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "components": {
                    "database": True,
                    "memory_store": True,
                    "debate_orchestrator": True
                },
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
    }
