"""
Middleware para CORS (Cross-Origin Resource Sharing).

Configura CORS para permitir requests desde diferentes dominios,
especialmente importante para demos y desarrollo.
"""

from fastapi.middleware.cors import CORSMiddleware


def configure_cors(app) -> None:
    """
    Configura CORS en la aplicación FastAPI.
    
    Args:
        app: Instancia de FastAPI
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # React development server
            "http://localhost:8080",  # Vue.js development server  
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8080",
            # En producción, especificar dominios exactos
            # "https://yourdomain.com",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
