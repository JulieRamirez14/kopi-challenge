"""
Implementación básica funcional del Debate Orchestrator.
Versión simplificada para hacer funcionar el API rápidamente.
"""

import random
from typing import Optional

from src.domain.services.debate_strategy import DebateContext, PersonalityType
from src.domain.services.personalities import (
    ConspiracyTheoristStrategy,
    PopulistStrategy,
    SkepticalScientistStrategy,
)


class DebateOrchestrator:
    """Basic service for orchestrating debates."""
    
    def __init__(self):
        """Initialize with basic personalities."""
        self._personalities = {
            PersonalityType.CONSPIRACY_THEORIST: ConspiracyTheoristStrategy(),
            PersonalityType.SKEPTICAL_SCIENTIST: SkepticalScientistStrategy(),
            PersonalityType.POPULIST: PopulistStrategy(),
        }
    
    def generate_bot_response(
        self,
        conversation=None, 
        user_message=None,
        preferred_personality: Optional[str] = None
    ) -> str:
        """Generate persuasive response maintaining consistent personality."""
        user_msg_str = str(user_message) if user_message else "general discussion"
        user_msg = user_msg_str.lower()
        
        # Mantener personalidad consistente en conversaciones existentes
        if conversation and hasattr(conversation, 'bot_personality_type') and conversation.bot_personality_type:
            try:
                personality_type = PersonalityType(conversation.bot_personality_type)
            except ValueError:
                personality_type = self._select_personality_by_topic(user_msg)
        elif preferred_personality:
            try:
                personality_type = PersonalityType(preferred_personality)
            except ValueError:
                personality_type = self._select_personality_by_topic(user_msg)
        else:
            personality_type = self._select_personality_by_topic(user_msg)
        
        # Save personality in new conversation for consistency
        if conversation and hasattr(conversation, 'bot_personality_type') and not conversation.bot_personality_type:
            conversation.bot_personality_type = personality_type.value
        
        personality = self._personalities[personality_type]
        
        # Crear contexto rico para respuesta persuasiva
        context = DebateContext(
            topic=self._extract_topic(user_msg_str),
            user_message=user_msg_str,
            bot_stance=self._get_opposing_stance(user_msg, personality_type),
            conversation_history=self._get_conversation_context(conversation)
        )
        
        return personality.generate_response(context)
    
    def _select_personality_by_topic(self, user_msg: str) -> PersonalityType:
        """Select most appropriate personality for the topic."""
        # Specific topics for each personality
        if any(word in user_msg for word in ["vaccine", "vaccination", "pharma", "medicine", "health", "immunity"]):
            return PersonalityType.CONSPIRACY_THEORIST
        elif any(word in user_msg for word in ["climate", "warming", "carbon", "environment", "green", "fossil"]):
            return PersonalityType.SKEPTICAL_SCIENTIST  
        elif any(word in user_msg for word in ["economic", "capitalism", "market", "business", "job", "worker", "education", "immigration", "elite"]):
            return PersonalityType.POPULIST
        else:
            # Para temas generales, seleccionar aleatoriamente pero de manera consistente
            return random.choice(list(PersonalityType))
    
    def _extract_topic(self, user_message: str) -> str:
        """Extract main topic from message."""
        # Simplified: return first key words
        return user_message[:100]
    
    def _get_opposing_stance(self, user_msg: str, personality: PersonalityType) -> str:
        """Define opposing stance that bot should take."""
        if personality == PersonalityType.CONSPIRACY_THEORIST:
            return "skeptical_of_mainstream_narrative"
        elif personality == PersonalityType.SKEPTICAL_SCIENTIST:
            return "methodologically_critical"  
        else:  # POPULIST
            return "pro_common_people_anti_elite"
    
    def _get_conversation_context(self, conversation) -> list:
        """Get context from previous conversations."""
        # Simplified: return empty list for now
        return []
    
    def get_initial_stance(self, topic: str) -> str:
        """Generate basic initial stance."""
        personality = random.choice(list(self._personalities.values()))
        return personality.get_initial_stance(topic)