"""
Tests unitarios para las entidades del dominio.

Valida el comportamiento de las entidades principales del sistema.
"""

import pytest
from datetime import datetime

from src.domain import Conversation, ConversationId, Message, MessageRole


class TestConversationId:
    """Tests para el value object ConversationId."""
    
    def test_generate_creates_unique_ids(self):
        """Test que generate() crea IDs únicos."""
        id1 = ConversationId.generate()
        id2 = ConversationId.generate()
        
        assert id1 != id2
        assert len(str(id1)) == 36  # UUID format
        assert str(id1) != str(id2)
    
    def test_from_string_with_valid_uuid(self):
        """Test que from_string() acepta UUIDs válidos."""
        uuid_str = "123e4567-e89b-12d3-a456-426614174000"
        conversation_id = ConversationId.from_string(uuid_str)
        
        assert str(conversation_id) == uuid_str
    
    def test_from_string_with_invalid_uuid_raises_error(self):
        """Test que from_string() rechaza UUIDs inválidos."""
        with pytest.raises(ValueError, match="Invalid UUID format"):
            ConversationId.from_string("invalid-uuid")
    
    def test_from_string_with_empty_string_raises_error(self):
        """Test que from_string() rechaza strings vacíos."""
        with pytest.raises(ValueError, match="cannot be empty"):
            ConversationId.from_string("")
    
    def test_equality(self):
        """Test que dos ConversationIds con el mismo valor son iguales."""
        uuid_str = "123e4567-e89b-12d3-a456-426614174000"
        id1 = ConversationId.from_string(uuid_str)
        id2 = ConversationId.from_string(uuid_str)
        
        assert id1 == id2


class TestMessage:
    """Tests para la entidad Message."""
    
    def test_create_user_message(self):
        """Test creación de mensaje de usuario."""
        timestamp = datetime.now()
        message = Message(
            role=MessageRole.USER,
            content="Hello, bot!",
            timestamp=timestamp
        )
        
        assert message.role == MessageRole.USER
        assert message.content == "Hello, bot!"
        assert message.timestamp == timestamp
        assert message.is_from_user is True
        assert message.is_from_bot is False
    
    def test_create_bot_message(self):
        """Test creación de mensaje de bot."""
        timestamp = datetime.now()
        message = Message(
            role=MessageRole.BOT,
            content="Hello, human!",
            timestamp=timestamp
        )
        
        assert message.role == MessageRole.BOT
        assert message.content == "Hello, human!"
        assert message.is_from_user is False
        assert message.is_from_bot is True
    
    def test_empty_content_raises_error(self):
        """Test que contenido vacío genera error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Message(
                role=MessageRole.USER,
                content="",
                timestamp=datetime.now()
            )
    
    def test_whitespace_only_content_raises_error(self):
        """Test que solo espacios en blanco genera error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Message(
                role=MessageRole.USER,
                content="   \n\t   ",
                timestamp=datetime.now()
            )
    
    def test_content_too_long_raises_error(self):
        """Test que contenido muy largo genera error."""
        long_content = "a" * 2001  # Excede el límite de 2000 caracteres
        
        with pytest.raises(ValueError, match="too long"):
            Message(
                role=MessageRole.USER,
                content=long_content,
                timestamp=datetime.now()
            )
    
    def test_content_is_trimmed(self):
        """Test que el contenido se limpia de espacios."""
        message = Message(
            role=MessageRole.USER,
            content="  Hello, bot!  ",
            timestamp=datetime.now()
        )
        
        assert message.content == "Hello, bot!"
    
    def test_word_count(self):
        """Test del contador de palabras."""
        message = Message(
            role=MessageRole.USER,
            content="Hello world, this is a test message",
            timestamp=datetime.now()
        )
        
        assert message.word_count == 7  # "Hello world, this is a test message" = 7 palabras
    
    def test_contains_keywords(self):
        """Test de búsqueda de palabras clave."""
        message = Message(
            role=MessageRole.USER,
            content="I think vaccines are important for public health",
            timestamp=datetime.now()
        )
        
        assert message.contains_keywords(["vaccines", "health"]) is True
        assert message.contains_keywords(["VACCINES"]) is True  # Case insensitive
        assert message.contains_keywords(["aliens", "conspiracy"]) is False
    
    def test_to_dict(self):
        """Test de conversión a diccionario."""
        message = Message(
            role=MessageRole.USER,
            content="Test message",
            timestamp=datetime.now()
        )
        
        result = message.to_dict()
        
        assert result == {
            "role": "user",
            "message": "Test message"
        }


class TestConversation:
    """Tests para la entidad Conversation."""
    
    def test_create_conversation(self):
        """Test creación básica de conversación."""
        conversation_id = ConversationId.generate()
        created_at = datetime.now()
        
        conversation = Conversation(
            id=conversation_id,
            created_at=created_at
        )
        
        assert conversation.id == conversation_id
        assert conversation.created_at == created_at
        assert conversation.is_new_conversation is True
        assert len(conversation.messages) == 0
        assert conversation.topic is None
        assert conversation.bot_position is None
    
    def test_add_user_message(self):
        """Test agregar mensaje de usuario."""
        conversation = Conversation(
            id=ConversationId.generate(),
            created_at=datetime.now()
        )
        
        message = conversation.add_user_message("Hello, bot!")
        
        assert len(conversation.messages) == 1
        assert message.role == MessageRole.USER
        assert message.content == "Hello, bot!"
        assert conversation.is_new_conversation is False
    
    def test_first_message_extracts_topic(self):
        """Test que el primer mensaje extrae el tema."""
        conversation = Conversation(
            id=ConversationId.generate(),
            created_at=datetime.now()
        )
        
        conversation.add_user_message("I think vaccines are safe and effective")
        
        assert conversation.topic == "vaccines and public health"
        assert "vaccination" in conversation.bot_position or "pharma" in conversation.bot_position.lower()
    
    def test_add_bot_message(self):
        """Test agregar mensaje de bot."""
        conversation = Conversation(
            id=ConversationId.generate(),
            created_at=datetime.now()
        )
        
        # Agregar mensaje de usuario primero
        conversation.add_user_message("Hello!")
        
        # Agregar respuesta de bot
        bot_message = conversation.add_bot_message("Hello, human!")
        
        assert len(conversation.messages) == 2
        assert bot_message.role == MessageRole.BOT
        assert bot_message.content == "Hello, human!"
    
    def test_message_count_and_exchange_count(self):
        """Test contadores de mensajes e intercambios."""
        conversation = Conversation(
            id=ConversationId.generate(),
            created_at=datetime.now()
        )
        
        assert conversation.message_count == 0
        assert conversation.exchange_count == 0
        
        conversation.add_user_message("Message 1")
        assert conversation.message_count == 1
        assert conversation.exchange_count == 0  # No hay respuesta del bot aún
        
        conversation.add_bot_message("Response 1")
        assert conversation.message_count == 2
        assert conversation.exchange_count == 1  # Primer intercambio completo
        
        conversation.add_user_message("Message 2")
        conversation.add_bot_message("Response 2")
        assert conversation.message_count == 4
        assert conversation.exchange_count == 2
    
    def test_get_recent_messages_respects_limit(self):
        """Test que get_recent_messages respeta el límite."""
        conversation = Conversation(
            id=ConversationId.generate(),
            created_at=datetime.now(),
            max_history=2  # Límite bajo para testing
        )
        
        # Agregar más mensajes que el límite
        for i in range(6):
            conversation.add_user_message(f"User message {i}")
            conversation.add_bot_message(f"Bot response {i}")
        
        recent_messages = conversation.get_recent_messages()
        
        # Debe tener máximo 4 mensajes (2 intercambios * 2 mensajes)
        assert len(recent_messages) <= 4
        
        # Los mensajes deben ser los más recientes
        assert "message 4" in recent_messages[-2].content or "message 5" in recent_messages[-2].content
    
    def test_get_messages_for_api(self):
        """Test formato de mensajes para API."""
        conversation = Conversation(
            id=ConversationId.generate(),
            created_at=datetime.now()
        )
        
        conversation.add_user_message("Hello!")
        conversation.add_bot_message("Hi there!")
        
        api_messages = conversation.get_messages_for_api()
        
        assert len(api_messages) == 2
        assert api_messages[0] == {"role": "user", "message": "Hello!"}
        assert api_messages[1] == {"role": "bot", "message": "Hi there!"}
    
    def test_last_messages_properties(self):
        """Test propiedades de último mensaje."""
        conversation = Conversation(
            id=ConversationId.generate(),
            created_at=datetime.now()
        )
        
        assert conversation.last_user_message is None
        assert conversation.last_bot_message is None
        
        user_msg = conversation.add_user_message("User message")
        assert conversation.last_user_message == user_msg
        assert conversation.last_bot_message is None
        
        bot_msg = conversation.add_bot_message("Bot message")
        assert conversation.last_user_message == user_msg
        assert conversation.last_bot_message == bot_msg
