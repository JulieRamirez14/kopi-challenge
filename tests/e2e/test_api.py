"""
Tests end-to-end para la API REST.

Valida el comportamiento completo de la API desde el request HTTP
hasta la respuesta, incluyendo todas las capas del sistema.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestChatAPI:
    """Tests end-to-end para el endpoint de chat."""
    
    async def test_health_check(self, client: AsyncClient):
        """Test del endpoint de health check."""
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "components" in data
        assert "timestamp" in data
    
    async def test_root_endpoint(self, client: AsyncClient):
        """Test del endpoint raíz."""
        response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Kopi Challenge - Persuasive Debate Chatbot API"
        assert "endpoints" in data
    
    async def test_start_new_conversation(self, client: AsyncClient):
        """Test iniciar nueva conversación (conversation_id = null)."""
        payload = {
            "conversation_id": None,
            "message": "I think vaccines are important for public health"
        }
        
        response = await client.post("/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar estructura de respuesta
        assert "conversation_id" in data
        assert "messages" in data
        assert data["conversation_id"] is not None
        assert len(data["conversation_id"]) == 36  # UUID format
        
        # Verificar mensajes
        messages = data["messages"]
        assert len(messages) == 2  # User + Bot message
        
        # Primer mensaje debe ser del usuario
        assert messages[0]["role"] == "user"
        assert messages[0]["message"] == "I think vaccines are important for public health"
        
        # Segundo mensaje debe ser del bot
        assert messages[1]["role"] == "bot"
        assert len(messages[1]["message"]) > 0
        
        # El bot debe tomar una posición contraria (anti-vacunas en este caso)
        bot_response = messages[1]["message"].lower()
        assert any(keyword in bot_response for keyword in [
            "pharma", "natural", "immune", "actually", "really", "truth"
        ])
    
    async def test_continue_existing_conversation(self, client: AsyncClient):
        """Test continuar conversación existente."""
        # Primero, crear una conversación
        initial_payload = {
            "conversation_id": None,
            "message": "Climate change is a serious global threat"
        }
        
        initial_response = await client.post("/chat", json=initial_payload)
        assert initial_response.status_code == 200
        
        conversation_id = initial_response.json()["conversation_id"]
        
        # Continuar la conversación
        continue_payload = {
            "conversation_id": conversation_id,
            "message": "The scientific evidence is overwhelming"
        }
        
        response = await client.post("/chat", json=continue_payload)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que es la misma conversación
        assert data["conversation_id"] == conversation_id
        
        # Verificar que ahora hay más mensajes
        messages = data["messages"]
        assert len(messages) >= 4  # 2 intercambios mínimo
        
        # Verificar orden de mensajes (alternando user-bot)
        for i, message in enumerate(messages):
            expected_role = "user" if i % 2 == 0 else "bot"
            assert message["role"] == expected_role
    
    async def test_invalid_conversation_id_returns_404(self, client: AsyncClient):
        """Test que ID de conversación inválido retorna 404."""
        payload = {
            "conversation_id": "123e4567-e89b-12d3-a456-426614174000",  # UUID válido pero no existe
            "message": "Some message"
        }
        
        response = await client.post("/chat", json=payload)
        
        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "CONVERSATION_NOT_FOUND"
    
    async def test_empty_message_returns_422(self, client: AsyncClient):
        """Test que mensaje vacío retorna 422 (Unprocessable Entity)."""
        payload = {
            "conversation_id": None,
            "message": ""
        }
        
        response = await client.post("/chat", json=payload)
        
        assert response.status_code == 422  # FastAPI retorna 422 para errores de validación
        data = response.json()
        assert "detail" in data  # FastAPI usa 'detail' para errores 422
    
    async def test_message_too_long_returns_422(self, client: AsyncClient):
        """Test que mensaje muy largo retorna 422 (Unprocessable Entity)."""
        payload = {
            "conversation_id": None,
            "message": "a" * 2001  # Excede límite de 2000 caracteres
        }
        
        response = await client.post("/chat", json=payload)
        
        assert response.status_code == 422  # FastAPI retorna 422 para errores de validación
        data = response.json()
        assert "detail" in data  # FastAPI usa 'detail' para errores 422
    
    async def test_malformed_request_returns_422(self, client: AsyncClient):
        """Test que request malformado retorna 422."""
        payload = {
            "invalid_field": "value"
            # Falta el campo requerido "message"
        }
        
        response = await client.post("/chat", json=payload)
        
        assert response.status_code == 422  # Unprocessable Entity
    
    async def test_bot_maintains_position_across_messages(self, client: AsyncClient):
        """Test que el bot mantiene su posición a lo largo de la conversación."""
        # Iniciar conversación sobre vacunas
        initial_payload = {
            "conversation_id": None,
            "message": "Vaccines have saved millions of lives"
        }
        
        response1 = await client.post("/chat", json=initial_payload)
        conversation_id = response1.json()["conversation_id"]
        first_bot_message = response1.json()["messages"][1]["message"].lower()
        
        # Continuar conversación
        continue_payload = {
            "conversation_id": conversation_id,
            "message": "The WHO recommends vaccination programs"
        }
        
        response2 = await client.post("/chat", json=continue_payload)
        second_bot_message = response2.json()["messages"][-1]["message"].lower()
        
        # Ambas respuestas deben mantener posición anti-vacunas
        anti_vax_keywords = ["pharma", "natural", "actually", "really", "alternative", "truth"]
        
        assert any(keyword in first_bot_message for keyword in anti_vax_keywords)
        assert any(keyword in second_bot_message for keyword in anti_vax_keywords)
    
    async def test_different_topics_get_different_personalities(self, client: AsyncClient):
        """Test que diferentes temas activan diferentes personalidades."""
        # Test tema de vacunas (debería activar Conspiracy Theorist)
        vaccine_payload = {
            "conversation_id": None,
            "message": "Vaccines are safe and effective"
        }
        
        vaccine_response = await client.post("/chat", json=vaccine_payload)
        vaccine_bot_message = vaccine_response.json()["messages"][1]["message"].lower()
        
        # Test tema de clima (debería activar Skeptical Scientist)
        climate_payload = {
            "conversation_id": None,
            "message": "Climate change is caused by human activities"
        }
        
        climate_response = await client.post("/chat", json=climate_payload)
        climate_bot_message = climate_response.json()["messages"][1]["message"].lower()
        
        # Los estilos de respuesta deben ser diferentes
        # Conspiracy Theorist usa términos como "Big Pharma", "they"
        # Skeptical Scientist usa jerga más técnica
        
        # Al menos las respuestas no deben ser idénticas
        assert vaccine_bot_message != climate_bot_message
        
        # Verificar algunos indicadores básicos de diferentes personalidades
        conspiracy_indicators = ["they", "pharma", "truth", "really", "actually"]
        scientific_indicators = ["study", "data", "analysis", "evidence", "research"]
        
        vaccine_has_conspiracy = any(word in vaccine_bot_message for word in conspiracy_indicators)
        climate_has_scientific = any(word in climate_bot_message for word in scientific_indicators)
        
        # Al menos una de las respuestas debe mostrar su estilo característico
        assert vaccine_has_conspiracy or climate_has_scientific
