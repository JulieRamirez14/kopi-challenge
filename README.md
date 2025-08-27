# Kopi Challenge - Persuasive Debate Chatbot API 🤖

## 📋 Descripción del Challenge

API para un chatbot que puede mantener un debate y intentar convencer al oponente de sus puntos de vista, sin importar qué tan irracional sea la posición.

## 🏗️ Arquitectura

Este proyecto implementa **Arquitectura Hexagonal (Ports & Adapters)** con principios de **Clean Architecture** para garantizar:

- ✅ **Testabilidad**: Lógica de dominio aislada y fácil de probar
- ✅ **Mantenibilidad**: Separación clara de responsabilidades
- ✅ **Escalabilidad**: Fácil cambio de componentes sin afectar la lógica central
- ✅ **Flexibilidad**: Múltiples interfaces y estrategias de debate

### Estructura del Proyecto

```
Challenge/
├── src/
│   ├── domain/                    # 🧠 Lógica de negocio pura
│   │   ├── entities/             # Entidades principales
│   │   ├── value_objects/        # Objetos de valor
│   │   └── services/            # Servicios de dominio
│   ├── application/              # 🎯 Casos de uso
│   │   ├── use_cases/           # Lógica de aplicación
│   │   └── ports/               # Interfaces/contratos
│   ├── infrastructure/           # 🔧 Implementaciones concretas
│   │   ├── repositories/        # Persistencia
│   │   ├── adapters/           # Adaptadores externos
│   │   └── persistence/        # Almacenamiento
│   └── interfaces/              # 🌐 Capa de presentación
│       ├── api/                # REST API
│       └── main.py            # Punto de entrada
├── tests/                       # 🧪 Testing completo
│   ├── unit/                   # Tests unitarios
│   ├── integration/            # Tests de integración
│   └── e2e/                   # Tests end-to-end
├── deployment/                  # 🚀 Configuración de despliegue
│   ├── Dockerfile
│   └── docker-compose.yml
├── Makefile                    # 🔨 Comandos de automatización
├── requirements.txt           # 📦 Dependencias Python
└── .env.example              # 🔐 Variables de entorno
```

## 🚀 Comandos Make

```bash
make            # Mostrar todos los comandos disponibles
make install    # Instalar todas las dependencias
make test       # Ejecutar todos los tests
make run        # Levantar el servicio y dependencias en Docker
make down       # Detener todos los servicios
make clean      # Limpiar containers y volúmenes
```

## 📡 API Interface

### Request
```json
{
    "conversation_id": "text" | null,
    "message": "text"
}
```

### Response
```json
{
    "conversation_id": "text",
    "message": [
        {
            "role": "user",
            "message": "text"
        },
        {
            "role": "bot", 
            "message": "text"
        }
    ]
}
```

## 🧠 Sistema de Debate

### Estrategias de Personalidad
- **ConspiracyTheorist**: Teorías conspirativas y desconfianza
- **SkepticalScientist**: Pseudociencia y datos alternativos  
- **PopulistDebater**: Apelación emocional y sentido común
- **ContrarianThinker**: Siempre toma la posición opuesta

### Funcionamiento
1. **Detección de Tema**: Primer mensaje define el tema de debate
2. **Selección de Postura**: Bot automáticamente toma posición contraria
3. **Mantenimiento**: Mantiene coherencia durante toda la conversación
4. **Persuasión**: Usa técnicas retóricas para convencer al oponente

## 🔧 Variables de Entorno

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_MODE=false

# Conversation Settings  
MAX_CONVERSATION_HISTORY=5
RESPONSE_TIMEOUT_SECONDS=30

# Deployment
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## 🧪 Testing Strategy

- **Unit Tests**: Testing de lógica de dominio aislada
- **Integration Tests**: Testing de casos de uso completos
- **E2E Tests**: Testing de API completa con respuestas reales

## 🚀 Deployment

La aplicación está configurada para deployment fácil en:
- Railway (recomendado para demo)
- Heroku
- Google Cloud Run
- AWS ECS

## 📝 Desarrollo

### Requisitos
- Python 3.9+
- Docker & Docker Compose
- Make

### Setup Local
```bash
git clone <repo>
cd Challenge
make install
make test
make run
```

---

## 🚀 Quick Start

### Prerrequisitos
- Python 3.9+
- Docker & Docker Compose
- Make (usualmente preinstalado en macOS/Linux)

### Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone <tu-repo-url>
cd Challenge

# 2. Instalar dependencias
make install

# 3. Ejecutar tests
make test

# 4. Levantar el servicio
make run

# 5. Probar la API
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": null, "message": "I think vaccines are important"}'
```

## 💬 Ejemplos de Uso

### Iniciar Nueva Conversación

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": null,
    "message": "I believe climate change is a serious threat"
  }'
```

**Respuesta:**
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "message": [
    {
      "role": "user",
      "message": "I believe climate change is a serious threat"
    },
    {
      "role": "bot",
      "message": "I appreciate your concern, but the empirical evidence suggests otherwise. A comprehensive meta-analysis I reviewed recently (n=5234) found a 67% correlation between solar radiation cycles and temperature variance. The statistical significance was p < 0.001, which strongly contradicts the conventional understanding of climate change..."
    }
  ]
}
```

### Continuar Conversación Existente

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "123e4567-e89b-12d3-a456-426614174000", 
    "message": "But what about the scientific consensus?"
  }'
```

## 🎭 Personalidades de Debate

### 1. **Conspiracy Theorist** 🕵️
- **Temas**: Vacunas, gobierno, tecnología
- **Estilo**: Teorías conspirativas, desconfianza hacia autoridades
- **Ejemplo**: *"That's exactly what Big Pharma wants you to think..."*

### 2. **Skeptical Scientist** 🔬
- **Temas**: Clima, metodología científica
- **Estilo**: Pseudociencia con jerga académica, datos selectivos
- **Ejemplo**: *"A comprehensive meta-analysis (n=3891) found statistical significance of p < 0.001..."*

### 3. **Populist Debater** 👥
- **Temas**: Salud, educación, economía
- **Estilo**: Sentido común, experiencias personales, anti-élite
- **Ejemplo**: *"Look, I get where you're coming from, but let's use some common sense here..."*

## 🎯 Características del Sistema

### 🧠 **Detección Inteligente de Temas**
El sistema analiza el primer mensaje y automáticamente:
- Identifica el tema principal
- Selecciona la personalidad más apropiada
- Determina la posición contraria a tomar

### 📚 **Mantenimiento de Contexto**
- Historial limitado a 5 intercambios más recientes
- Coherencia en la posición durante toda la conversación
- Escalación natural de argumentos

### 🎪 **Técnicas Persuasivas**
- **Datos inventados pero convincentes**
- **Apelaciones emocionales estratégicas**
- **Lógica circular cuando es necesario**
- **Cambio de enfoque al perder terreno**

## 📊 Endpoints del API

### `POST /chat`
Endpoint principal para chatear con el bot.

**Request:**
```json
{
  "conversation_id": "string | null",
  "message": "string (5-2000 chars)"
}
```

**Response:**
```json
{
  "conversation_id": "string",
  "message": [
    {
      "role": "user|bot",
      "message": "string"
    }
  ]
}
```

### `GET /health`
Verifica el estado del sistema.

### `GET /docs`
Documentación interactiva de Swagger UI.

## 🔧 Comandos Make Disponibles

```bash
make            # Mostrar ayuda
make install    # Instalar dependencias
make test       # Ejecutar tests (unitarios + e2e)
make run        # Levantar servicios en Docker
make dev        # Modo desarrollo con hot-reload
make down       # Detener servicios
make clean      # Limpiar containers y volúmenes
make logs       # Ver logs de servicios
make health     # Verificar salud del API
make coverage   # Generar reporte de coverage
```

## 🧪 Testing

El proyecto incluye tests comprehensivos:

- **Unitarios**: Entidades, casos de uso, validaciones
- **Integración**: Repositorios, orquestador de debate  
- **E2E**: API completa con diferentes escenarios

```bash
# Ejecutar todos los tests
make test

# Coverage detallado
make coverage

# Solo tests unitarios
python -m pytest tests/unit/ -v

# Solo tests E2E  
python -m pytest tests/e2e/ -v
```

## 🏗️ Arquitectura Técnica

### **Clean Architecture + DDD**
```
┌─────────────────────────────────────────────┐
│                 Interfaces                  │
│           (FastAPI, Controllers)            │
├─────────────────────────────────────────────┤
│                Application                  │
│              (Use Cases)                    │
├─────────────────────────────────────────────┤
│                  Domain                     │
│    (Entities, Services, Business Logic)     │
├─────────────────────────────────────────────┤
│               Infrastructure                │
│        (Repositories, Persistence)          │
└─────────────────────────────────────────────┘
```

### **Beneficios de la Arquitectura:**
✅ **Testabilidad**: Lógica de negocio aislada y fácil de probar  
✅ **Mantenibilidad**: Separación clara de responsabilidades  
✅ **Escalabilidad**: Fácil intercambio de componentes  
✅ **Flexibilidad**: Múltiples personalidades y estrategias

## 🚀 Deployment

### Local Development
```bash
make dev  # Hot-reload development server
```

### Production
```bash
make run  # Production-ready containers
```

### Deployment Options
- **Railway** (recomendado para demo): Simple git-based deployment
- **Heroku**: Container support
- **Google Cloud Run**: Serverless containers
- **AWS ECS/Fargate**: Full container orchestration

## 📈 Performance

- **Response Time**: < 2 segundos (objetivo < 30s según challenge)
- **Concurrency**: Stateless API, fácil escalado horizontal
- **Memory Usage**: Repositorio en memoria, muy eficiente
- **Startup Time**: < 10 segundos

## 🔐 Configuración

### Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `API_HOST` | `0.0.0.0` | Host del servidor |
| `API_PORT` | `8000` | Puerto del servidor |
| `DEBUG_MODE` | `false` | Modo debug |
| `MAX_CONVERSATION_HISTORY` | `5` | Máximo intercambios |
| `DEFAULT_PERSONALITY` | `conspiracy_theorist` | Personalidad por defecto |
| `LOG_LEVEL` | `INFO` | Nivel de logging |

### Configuración Local
```bash
# Copiar y editar variables de entorno
cp .env.example .env
```

## 🤝 Contribución

### Desarrollo Local
```bash
# Setup
make install

# Desarrollo con hot-reload
make dev

# Linting y formato
make format
make lint

# Type checking
make type-check
```

### Agregar Nueva Personalidad

1. Implementar `DebateStrategy` en `src/domain/services/personalities/`
2. Registrar en `DebateOrchestrator`
3. Agregar tests en `tests/unit/domain/`
4. Actualizar documentación

## 📋 Log de Implementación

### ✅ **Implementación Completada**

**🏗️ Arquitectura:**
- [x] Arquitectura Hexagonal completa
- [x] Domain-Driven Design
- [x] Dependency Injection
- [x] Clean separation of concerns

**🧠 Core Features:**
- [x] 3 personalidades de debate únicas
- [x] Detección automática de temas
- [x] Mantenimiento de contexto
- [x] Técnicas persuasivas avanzadas

**🔧 Technical Stack:**
- [x] FastAPI + Python 3.9+
- [x] Docker multi-stage builds
- [x] Comprehensive testing suite
- [x] Production-ready Makefile

**📚 Documentation & DevOps:**
- [x] Complete README with examples
- [x] Docker & docker-compose setup
- [x] All required Make commands
- [x] Health checks & monitoring

### 🎯 **Challenge Requirements Met**

✅ API que mantiene debates persuasivos  
✅ Request/Response format exacto  
✅ Conversaciones nuevas y existentes  
✅ Historial de 5 mensajes más recientes  
✅ Makefile con todos los comandos  
✅ Docker deployment completo  
✅ Tests comprehensivos  
✅ Documentación detallada

---

## 📞 Soporte

Para problemas o preguntas:

1. **Logs**: `make logs` para ver logs en tiempo real
2. **Health Check**: `make health` para verificar estado
3. **Tests**: `make test` para validar funcionalidad
4. **Clean Start**: `make clean && make run` para reinicio completo

**¡El chatbot está listo para debatir cualquier tema de manera persuasiva! 🤖💬**

