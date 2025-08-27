# Interface Layer - External interfaces (API, CLI, etc.)

# Re-export main FastAPI app for easy import
from .main import app

__all__ = [
    "app",
]