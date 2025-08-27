"""
Implementación básica funcional de debate strategy.
Versión simplificada para hacer funcionar el API rápidamente.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from abc import ABC, abstractmethod


class PersonalityType(Enum):
    """Tipos de personalidad disponibles para el debate."""
    CONSPIRACY_THEORIST = "conspiracy_theorist"
    SKEPTICAL_SCIENTIST = "skeptical_scientist"
    POPULIST = "populist"


@dataclass
class DebateContext:
    """Context for generating debate responses."""
    topic: str
    user_message: str
    bot_stance: str
    conversation_history: List[str]


class DebateStrategy(ABC):
    """Estrategia base para personalidades de debate."""
    
    @abstractmethod
    def generate_response(self, context: DebateContext) -> str:
        """Genera una respuesta persuasiva."""
        pass
    
    @abstractmethod
    def get_initial_stance(self, topic: str) -> str:
        """Genera la postura inicial para un tema."""
        pass