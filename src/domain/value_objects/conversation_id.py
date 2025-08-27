"""
Value Object para el ID de conversación.

Un Value Object es inmutable y se define por sus atributos.
Encapsula la lógica de generación y validación de IDs de conversación.
"""

import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class ConversationId:
    """
    Representa un identificador único para una conversación.
    
    Características:
    - Inmutable (frozen=True)
    - Se define por su valor, no por identidad
    - Encapsula lógica de validación
    """
    
    value: str
    
    @classmethod
    def generate(cls) -> 'ConversationId':
        """Generate a new unique conversation ID."""
        return cls(value=str(uuid.uuid4()))
    
    @classmethod
    def from_string(cls, value: str) -> 'ConversationId':
        """
        Crea un ConversationId desde un string.
        
        Args:
            value: String que representa el ID
            
        Returns:
            ConversationId válido
            
        Raises:
            ValueError: Si el string no es un UUID válido
        """
        if not value or not value.strip():
            raise ValueError("ConversationId cannot be empty")
            
        # Validate that it's a valid UUID
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError(f"Invalid UUID format: {value}")
            
        return cls(value=value.strip())
    
    def __str__(self) -> str:
        """String representation of ID."""
        return self.value
    
    def __repr__(self) -> str:
        """Representation for debugging."""
        return f"ConversationId(value='{self.value}')"
