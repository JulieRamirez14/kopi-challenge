# Multi-stage Dockerfile para la Kopi Challenge Debate API
# Optimizado para tamaño y seguridad en producción

# Stage 1: Build environment
FROM python:3.9-slim as builder

# Metadatos
LABEL maintainer="Kopi Challenge"
LABEL description="Persuasive Debate Chatbot API"

# Variables de entorno para build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema para build
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /build

# Copiar archivos de dependencias
COPY requirements.txt pyproject.toml ./

# Crear virtual environment y instalar dependencias
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Stage 2: Production environment  
FROM python:3.9-slim as production

# Variables de entorno para runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app"

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /bin/bash appuser

# Instalar dependencias runtime mínimas
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar virtual environment desde stage builder
COPY --from=builder /opt/venv /opt/venv

# Crear directorio de aplicación
WORKDIR /app

# Copiar código de la aplicación
COPY src/ ./src/
COPY .env.example .env

# Cambiar ownership a appuser
RUN chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto
CMD ["uvicorn", "src.interfaces.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 3: Development environment
FROM production as development

# Cambiar de vuelta a root para instalar herramientas de desarrollo
USER root

# Instalar dependencias de desarrollo adicionales
RUN pip install \
    pytest \
    pytest-asyncio \
    pytest-cov \
    black \
    isort \
    mypy \
    flake8

# Instalar herramientas de debugging
RUN apt-get update && apt-get install -y \
    vim \
    htop \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Cambiar ownership
RUN chown -R appuser:appuser /opt/venv

# Volver a usuario no-root
USER appuser

# En desarrollo, usar reload automático
CMD ["uvicorn", "src.interfaces.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
