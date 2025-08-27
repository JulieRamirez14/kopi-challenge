"""
Main entry point for the FastAPI application.

Configures and exposes the REST API for the persuasive debate chatbot.
"""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from src.interfaces.api.controllers.chat_controller import ChatController
from src.interfaces.api.middleware.cors_middleware import configure_cors
from src.interfaces.api.middleware.error_handler import ErrorHandlerMiddleware
from src.interfaces.api.schemas.chat_schemas import ChatRequest, ChatResponse, ErrorResponse, HealthResponse

# Configure standard logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for the application lifecycle.
    
    Handles resource initialization and cleanup.
    """
    # Startup
    logger.info("Starting Kopi Challenge Debate API")
    
    try:
        # Resources can be initialized here if needed
        # (DB connections, caches, etc.)
        yield
    finally:
        # Cleanup
        logger.info("Shutting down Kopi Challenge Debate API")


# Create FastAPI application
app = FastAPI(
    title="Kopi Challenge - Persuasive Debate Chatbot API",
    description=(
        "API for a chatbot that can hold a debate and attempt to convince "
        "the opponent of its viewpoints, regardless of how irrational the position may be."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
configure_cors(app)

# Agregar middleware de manejo de errores
app.add_middleware(ErrorHandlerMiddleware)

# Inicializar controlador
chat_controller = ChatController()


@app.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Invalid input"},
        404: {"model": ErrorResponse, "description": "Not Found - Conversation not found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Chat with the debate bot",
    description=(
        "Main endpoint to chat with the debate bot. "
        "If conversation_id is null, starts a new conversation. "
        "If conversation_id is provided, continues the existing conversation."
    ),
)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Endpoint principal de chat.
    
    Args:
        request: Request con conversation_id (opcional) y mensaje
        
    Returns:
        Response con conversation_id y historial de mensajes
        
    Raises:
        HTTPException: Para diversos errores (400, 404, 500)
    """
    return await chat_controller.chat(request)


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Checks the health status of the application and its components.",
)
async def health_endpoint() -> HealthResponse:
    """
    Endpoint de health check.
    
    Returns:
        Estado de salud del sistema y componentes
    """
    health_data = await chat_controller.health_check()
    
    return HealthResponse(
        status=health_data["status"],
        components=health_data["components"],
        timestamp=health_data["timestamp"]
    )


@app.get(
    "/",
    summary="API Info",
    description="Basic information about the API.",
)
async def root_endpoint() -> Dict[str, Any]:
    """
    Root endpoint with API information.
    
    Returns:
        Basic API information
    """
    return {
        "name": "Kopi Challenge - Persuasive Debate Chatbot API",
        "version": "1.0.0",
        "description": "API para un chatbot que mantiene debates persuasivos",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "timestamp": datetime.now().isoformat(),
        "status": "operational"
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handler personalizado para 404s."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "NOT_FOUND",
            "message": "The requested resource was not found",
            "details": f"Path {request.url.path} does not exist"
        }
    )


@app.exception_handler(405)
async def method_not_allowed_handler(request, exc):
    """Handler personalizado para 405s."""
    return JSONResponse(
        status_code=405,
        content={
            "error": "METHOD_NOT_ALLOWED",
            "message": f"Method {request.method} is not allowed for this endpoint",
            "details": "Check the API documentation for allowed methods"
        }
    )


# Additional metadata for documentation
app.openapi_tags = [
    {
        "name": "chat",
        "description": "Operaciones de chat y debate con el bot",
    },
    {
        "name": "health",
        "description": "Endpoints de monitoreo y salud del sistema",
    },
]


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting development server")
    uvicorn.run(
        "src.interfaces.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
