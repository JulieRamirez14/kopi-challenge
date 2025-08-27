"""
Port para el repositorio de conversaciones.

Define la interfaz que debe implementar cualquier repositorio de conversaciones.
Esta es la inversión de dependencia - el dominio define qué necesita.
"""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain import Conversation, ConversationId


class ConversationRepository(ABC):
    """
    Interfaz abstracta para el repositorio de conversaciones.
    
    Esta interfaz permite que la capa de aplicación sea independiente
    de la implementación específica de persistencia.
    """
    
    @abstractmethod
    async def save(self, conversation: Conversation) -> None:
        """
        Guarda una conversación en el repositorio.
        
        Args:
            conversation: Conversación a guardar
            
        Raises:
            RepositoryException: Si no puede guardar la conversación
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, conversation_id: ConversationId) -> Optional[Conversation]:
        """
        Busca una conversación por su ID.
        
        Args:
            conversation_id: ID de la conversación a buscar
            
        Returns:
            Conversación encontrada o None si no existe
            
        Raises:
            RepositoryException: Si hay error en la búsqueda
        """
        pass
    
    @abstractmethod
    async def update(self, conversation: Conversation) -> None:
        """
        Actualiza una conversación existente.
        
        Args:
            conversation: Conversación con datos actualizados
            
        Raises:
            ConversationNotFoundException: Si la conversación no existe
            RepositoryException: Si hay error en la actualización
        """
        pass
    
    @abstractmethod
    async def delete(self, conversation_id: ConversationId) -> bool:
        """
        Elimina una conversación del repositorio.
        
        Args:
            conversation_id: ID de la conversación a eliminar
            
        Returns:
            True si se eliminó, False si no existía
            
        Raises:
            RepositoryException: Si hay error en la eliminación
        """
        pass
    
    @abstractmethod
    async def count_active_conversations(self) -> int:
        """
        Cuenta el número de conversaciones activas.
        
        Returns:
            Número de conversaciones en el repositorio
            
        Raises:
            RepositoryException: Si hay error en el conteo
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verifica la salud del repositorio.
        
        Returns:
            True si el repositorio está funcionando correctamente
        """
        pass
