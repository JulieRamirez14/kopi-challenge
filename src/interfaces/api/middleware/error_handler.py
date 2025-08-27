"""
Middleware for global error handling.

Captures unhandled exceptions and converts them into appropriate HTTP responses.
"""

import logging
import traceback
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware que captura y maneja errores globalmente.
    
    Convierte excepciones no manejadas en respuestas JSON estructuradas
    y registra información de debugging apropiada.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Procesa la request y maneja errores si ocurren.
        
        Args:
            request: Request HTTP entrante
            call_next: Siguiente middleware en la cadena
            
        Returns:
            Response HTTP (normal o de error)
        """
        try:
            # Log basic request info
            logger.info(f"Request started: {request.method} {request.url}")
            
            # Procesar request
            response = await call_next(request)
            
            logger.info(f"Request completed: {response.status_code}")
            
            return response
            
        except Exception as exc:
            logger.error(f"Unhandled exception: {type(exc).__name__}: {exc}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            
            # Determinar código de estado y mensaje apropiados
            if hasattr(exc, 'status_code'):
                status_code = exc.status_code
            else:
                status_code = 500
            
            error_response = {
                "error": "INTERNAL_ERROR",
                "message": "An internal server error occurred",
                "details": "Please try again later or contact support"
            }
            
            # En desarrollo, incluir más detalles del error
            if logger.isEnabledFor(logging.DEBUG):
                error_response["debug_info"] = {
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "traceback": traceback.format_exc().split('\n')
                }
            
            return JSONResponse(
                status_code=status_code,
                content=error_response
            )
