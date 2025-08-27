"""
Entidad Conversation del dominio.

Representa una conversación completa de debate con toda su lógica de negocio.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.domain.entities.message import Message, MessageRole
from src.domain.value_objects.conversation_id import ConversationId


@dataclass
class Conversation:
    """
    Entidad principal que representa una conversación de debate.
    
    Encapsula toda la lógica relacionada con:
    - Manejo del historial de mensajes (máximo 5 intercambios)
    - Detección del tema de debate
    - Determinación de la posición del bot
    - Estado de la conversación
    """
    
    id: ConversationId
    created_at: datetime
    messages: list[Message] = field(default_factory=list)
    topic: Optional[str] = None
    bot_position: Optional[str] = None
    bot_personality_type: Optional[str] = None  # To maintain consistency in conversation
    max_history: int = 5
    
    def __post_init__(self) -> None:
        """Post-initialization validations."""
        if self.max_history < 1:
            raise ValueError("max_history must be at least 1")
    
    @property
    def is_new_conversation(self) -> bool:
        """Check if this is a new conversation (no messages)."""
        return len(self.messages) == 0
    
    @property
    def last_user_message(self) -> Optional[Message]:
        """Get the last user message."""
        user_messages = [msg for msg in self.messages if msg.is_from_user]
        return user_messages[-1] if user_messages else None
    
    @property
    def last_bot_message(self) -> Optional[Message]:
        """Get the last bot message."""
        bot_messages = [msg for msg in self.messages if msg.is_from_bot]
        return bot_messages[-1] if bot_messages else None
    
    @property
    def message_count(self) -> int:
        """Total count of messages in conversation."""
        return len(self.messages)
    
    @property
    def exchange_count(self) -> int:
        """
        Cuenta los intercambios (pares de user-bot).
        
        Un intercambio completo = 1 mensaje de usuario + 1 respuesta del bot
        """
        user_count = len([msg for msg in self.messages if msg.is_from_user])
        bot_count = len([msg for msg in self.messages if msg.is_from_bot])
        return min(user_count, bot_count)
    
    def add_user_message(self, content: str, timestamp: Optional[datetime] = None) -> Message:
        """
        Añade un mensaje del usuario a la conversación.
        
        Args:
            content: Contenido del mensaje
            timestamp: Timestamp del mensaje (por defecto: now)
            
        Returns:
            El mensaje creado
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        message = Message(
            role=MessageRole.USER,
            content=content,
            timestamp=timestamp
        )
        
        # Si es el primer mensaje, extraer el tema
        if self.is_new_conversation:
            self._extract_topic_from_first_message(content)
        
        self.messages.append(message)
        self._maintain_history_limit()
        
        return message
    
    def add_bot_message(self, content: str, timestamp: Optional[datetime] = None) -> Message:
        """
        Añade un mensaje del bot a la conversación.
        
        Args:
            content: Contenido del mensaje
            timestamp: Timestamp del mensaje (por defecto: now)
            
        Returns:
            El mensaje creado
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        message = Message(
            role=MessageRole.BOT,
            content=content,
            timestamp=timestamp
        )
        
        self.messages.append(message)
        self._maintain_history_limit()
        
        return message
    
    def get_recent_messages(self, limit: Optional[int] = None) -> list[Message]:
        """
        Obtiene los mensajes más recientes.
        
        Args:
            limit: Número máximo de mensajes a retornar
                  (por defecto: max_history * 2 para incluir intercambios completos)
        
        Returns:
            Lista de mensajes más recientes
        """
        if limit is None:
            limit = self.max_history * 2  # user + bot messages
            
        return self.messages[-limit:] if limit > 0 else self.messages
    
    def get_messages_for_api(self) -> list[dict[str, str]]:
        """
        Obtiene los mensajes formateados para la respuesta del API.
        
        Returns:
            Lista de diccionarios con formato: {"role": "user|bot", "message": "..."}
        """
        recent_messages = self.get_recent_messages(self.max_history * 2)
        return [msg.to_dict() for msg in recent_messages]
    
    def _extract_topic_from_first_message(self, content: str) -> None:
        """
        Extrae el tema de debate del primer mensaje del usuario.
        
        Esta es lógica de dominio pura - simplificada para el challenge.
        En un sistema real podría usar NLP o AI para mejor detección.
        """
        # Simplified topic extraction logic
        self.topic = self._identify_topic_keywords(content)
        self.bot_position = self._determine_contrarian_position(self.topic)
    
    def _identify_topic_keywords(self, content: str) -> str:
        """
        Identifica palabras clave para determinar el tema.
        
        Args:
            content: Contenido del primer mensaje
            
        Returns:
            Tema identificado o tema genérico
        """
        content_lower = content.lower()
        
        # Mapeo de palabras clave a temas
        topic_keywords = {
            "vaccine": "vaccines and public health",
            "climate": "climate change",
            "earth": "earth shape and geography", 
            "government": "government and politics",
            "health": "health and medicine",
            "technology": "technology and society",
            "education": "education system",
            "economy": "economic policies",
            "science": "scientific methodology"
        }
        
        for keyword, topic in topic_keywords.items():
            if keyword in content_lower:
                return topic
                
        # Generic topic if no specific one is identified
        return "general debate topic"
    
    def _determine_contrarian_position(self, topic: str) -> str:
        """
        Determina la posición contraria que debe tomar el bot.
        
        Args:
            topic: Tema identificado
            
        Returns:
            Descripción de la posición contraria
        """
        contrarian_positions = {
            "vaccines and public health": "anti-vaccination and natural immunity advocate",
            "climate change": "climate change skeptic",
            "earth shape and geography": "flat earth proponent",
            "government and politics": "anti-establishment libertarian",
            "health and medicine": "alternative medicine advocate", 
            "technology and society": "technology skeptic",
            "education system": "homeschooling and alternative education advocate",
            "economic policies": "free market absolutist",
            "scientific methodology": "traditional wisdom and intuition advocate"
        }
        
        return contrarian_positions.get(topic, "devil's advocate contrarian")
    
    def _maintain_history_limit(self) -> None:
        """
        Mantiene el límite de historial eliminando los mensajes más antiguos.
        
        Preserva los intercambios completos (user-bot pairs).
        """
        if len(self.messages) <= self.max_history * 2:
            return
            
        # Calculate how many messages to remove maintaining complete exchanges
        excess_messages = len(self.messages) - (self.max_history * 2)
        
        # Remove from beginning to keep most recent ones
        if excess_messages > 0:
            self.messages = self.messages[excess_messages:]
    
    def __str__(self) -> str:
        """String representation of conversation."""
        return (
            f"Conversation({self.id}, topic='{self.topic}', "
            f"messages={len(self.messages)})"
        )
    
    def __repr__(self) -> str:
        """Representation for debugging."""
        return (
            f"Conversation(id={self.id!r}, topic='{self.topic}', "
            f"bot_position='{self.bot_position}', messages={len(self.messages)})"
        )

