"""
Entidad Message del dominio.

Representa un mensaje individual en una conversación de debate.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class MessageRole(str, Enum):
    """
    Roles disponibles para los mensajes.
    
    USER: Mensaje enviado por el usuario
    BOT: Mensaje generado por el chatbot
    """
    USER = "user"
    BOT = "bot"


@dataclass
class Message:
    """
    Entidad que representa un mensaje en una conversación.
    
    Una entidad se define por su identidad, no por sus atributos.
    Los mensajes tienen comportamiento relacionado con su contenido y rol.
    """
    
    role: MessageRole
    content: str
    timestamp: datetime
    id: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Post-initialization validations."""
        if not self.content or not self.content.strip():
            raise ValueError("Message content cannot be empty")
        
        if len(self.content.strip()) > 2000:
            raise ValueError("Message content too long (max 2000 characters)")
            
        # Limpiar el contenido
        self.content = self.content.strip()
    
    @property
    def is_from_user(self) -> bool:
        """Verifica si el mensaje es del usuario."""
        return self.role == MessageRole.USER
    
    @property  
    def is_from_bot(self) -> bool:
        """Verifica si el mensaje es del bot."""
        return self.role == MessageRole.BOT
    
    @property
    def word_count(self) -> int:
        """Cuenta las palabras en el mensaje."""
        return len(self.content.split())
    
    def contains_keywords(self, keywords: list[str]) -> bool:
        """
        Verifica si el mensaje contiene alguna de las palabras clave.
        
        Args:
            keywords: Lista de palabras clave a buscar
            
        Returns:
            True si contiene al menos una palabra clave
        """
        content_lower = self.content.lower()
        return any(keyword.lower() in content_lower for keyword in keywords)
    
    def to_dict(self) -> dict[str, str]:
        """
        Convierte el mensaje a diccionario para serialización.
        
        Returns:
            Diccionario con role y message (según spec del API)
        """
        return {
            "role": self.role.value,
            "message": self.content
        }
    
    def __str__(self) -> str:
        """String representation of the message."""
        return f"[{self.role.value.upper()}]: {self.content[:50]}..."
    
    def __repr__(self) -> str:
        """Representation for debugging."""
        return (
            f"Message(role={self.role}, content='{self.content[:30]}...', "
            f"timestamp={self.timestamp})"
        )
