"""
Almacén en memoria para conversaciones.

Implementación thread-safe de un almacén en memoria para el repositorio.
"""

import asyncio
from typing import Dict, Optional

from src.domain import Conversation, ConversationId
from src.infrastructure.exceptions import MemoryRepositoryException


class MemoryConversationStore:
    """
    Almacén en memoria thread-safe para conversaciones.
    
    Esta implementación usa un diccionario en memoria con locks
    para garantizar consistencia en operaciones concurrentes.
    """
    
    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}
        self._lock = asyncio.Lock()
    
    async def store(self, conversation: Conversation) -> None:
        """
        Almacena una conversación.
        
        Args:
            conversation: Conversación a almacenar
            
        Raises:
            MemoryRepositoryException: Si hay error en el almacenamiento
        """
        try:
            async with self._lock:
                self._conversations[str(conversation.id)] = conversation
        except Exception as e:
            raise MemoryRepositoryException(f"Failed to store conversation: {e}", "store")
    
    async def retrieve(self, conversation_id: ConversationId) -> Optional[Conversation]:
        """
        Recupera una conversación por ID.
        
        Args:
            conversation_id: ID de la conversación
            
        Returns:
            Conversación encontrada o None
            
        Raises:
            MemoryRepositoryException: Si hay error en la recuperación
        """
        try:
            async with self._lock:
                return self._conversations.get(str(conversation_id))
        except Exception as e:
            raise MemoryRepositoryException(f"Failed to retrieve conversation: {e}", "retrieve")
    
    async def update(self, conversation: Conversation) -> None:
        """
        Actualiza una conversación existente.
        
        Args:
            conversation: Conversación con datos actualizados
            
        Raises:
            MemoryRepositoryException: Si la conversación no existe o hay error
        """
        try:
            async with self._lock:
                conversation_id = str(conversation.id)
                
                if conversation_id not in self._conversations:
                    raise MemoryRepositoryException(
                        f"Conversation not found for update: {conversation_id}",
                        "update"
                    )
                
                self._conversations[conversation_id] = conversation
        except MemoryRepositoryException:
            raise
        except Exception as e:
            raise MemoryRepositoryException(f"Failed to update conversation: {e}", "update")
    
    async def delete(self, conversation_id: ConversationId) -> bool:
        """
        Elimina una conversación.
        
        Args:
            conversation_id: ID de la conversación a eliminar
            
        Returns:
            True si se eliminó, False si no existía
            
        Raises:
            MemoryRepositoryException: Si hay error en la eliminación
        """
        try:
            async with self._lock:
                conversation_id_str = str(conversation_id)
                
                if conversation_id_str in self._conversations:
                    del self._conversations[conversation_id_str]
                    return True
                
                return False
        except Exception as e:
            raise MemoryRepositoryException(f"Failed to delete conversation: {e}", "delete")
    
    async def count(self) -> int:
        """
        Cuenta el número de conversaciones almacenadas.
        
        Returns:
            Número total de conversaciones
            
        Raises:
            MemoryRepositoryException: Si hay error en el conteo
        """
        try:
            async with self._lock:
                return len(self._conversations)
        except Exception as e:
            raise MemoryRepositoryException(f"Failed to count conversations: {e}", "count")
    
    async def get_all_ids(self) -> list[str]:
        """
        Obtiene todos los IDs de conversaciones almacenadas.
        
        Returns:
            Lista de IDs de conversaciones
            
        Raises:
            MemoryRepositoryException: Si hay error obteniendo IDs
        """
        try:
            async with self._lock:
                return list(self._conversations.keys())
        except Exception as e:
            raise MemoryRepositoryException(f"Failed to get conversation IDs: {e}", "get_all_ids")
    
    async def clear(self) -> None:
        """
        Limpia todas las conversaciones (útil para testing).
        
        Raises:
            MemoryRepositoryException: Si hay error limpiando
        """
        try:
            async with self._lock:
                self._conversations.clear()
        except Exception as e:
            raise MemoryRepositoryException(f"Failed to clear conversations: {e}", "clear")
    
    async def health_check(self) -> bool:
        """
        Verifica la salud del almacén.
        
        Returns:
            True si está funcionando correctamente
        """
        try:
            async with self._lock:
                # Verificación básica de que el diccionario está accesible
                _ = len(self._conversations)
                return True
        except Exception:
            return False
