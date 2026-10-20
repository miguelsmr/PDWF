# Práctica 1.3 — Organización con APIRouter

**Alumno:** Miguel Luzón Prado

## Qué he hecho

En la práctica anterior todas las rutas estaban en `main.py`. Ahora cada recurso tiene su propio archivo dentro de `app/routers/`, usando `APIRouter` con su `prefix` y sus `tags`, y en `main.py` solo se crea la app y se incluyen los routers con `app.include_router(...)`.

Además he versionado la API: las rutas de negocio van con el prefijo `/api/v1`, así si algún día cambia la forma de la API se puede sacar una `/api/v2` sin romper lo que ya funciona.

## Estructura de carpetas

```
Practica1.3/
├── app/
│   ├── __init__.py
│   ├── main.py            # crea la app, registra el manejador de errores e incluye los routers
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py      # nombre, versión, prefijo /api/v1 y descripción de los tags
│   │   └── errores.py     # mensajes del error 422 en español
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py       # APIRouter(prefix="/tasks", tags=["tasks"])
│   │   ├── projects.py    # APIRouter(prefix="/projects", tags=["projects"])
│   │   └── health.py      # /health, /version y /ping
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py        # TaskCreate y TaskRead
│   │   └── project.py     # ProjectCreate y ProjectRead
│   └── models/
│       └── __init__.py    # vacío, aquí irán los modelos de SQLAlchemy
├── capturas/
├── README.md
└── requirements.txt
```

## Endpoints

- `POST /api/v1/tasks` → crea una tarea (simulada), devuelve 201
- `POST /api/v1/projects` → crea un proyecto (simulado), devuelve 201
- `GET /health`, `GET /version`, `GET /ping` → comprobar que la API funciona

Los nombres de los recursos van siempre en plural (`tasks`, `projects`), como en el documento del proyecto TaskFlow.

Las rutas de health no llevan `/api/v1` porque no son de negocio, solo sirven para comprobar que el servidor está levantado (por ejemplo desde Docker).

## Por qué esta estructura

- **routers/**: un archivo por recurso. Si tengo que tocar algo de las tareas sé que está en `tasks.py` y no tengo que buscar en un archivo enorme.
- **schemas/**: los datos que entran y salen de la API, separados por recurso igual que los routers.
- **models/**: de momento vacío, pero cuando metamos SQLAlchemy los modelos de la base de datos irán aquí, separados de los schemas.
- **core/**: lo que es común a toda la app (configuración y errores), para no repetirlo en cada router.

## Monolito frente a diseño modular

Con todo en `main.py` (monolito) al principio es más rápido, pero cuando la API crece el archivo se hace muy largo, es fácil romper algo sin querer y si trabajan dos personas a la vez se pisan los cambios en el mismo archivo.

Con el diseño modular cada parte está en su sitio: añadir un recurso nuevo (por ejemplo categorías) es crear `routers/categories.py` y añadir una línea en `main.py`, sin tocar lo que ya funciona. También es más fácil hacer pruebas de cada router por separado. El coste es que hay más archivos y carpetas, pero merece la pena en cuanto el proyecto tiene varios recursos, que es lo que va a pasar con TaskFlow.

## Cómo arrancarlo

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger en http://127.0.0.1:8000/docs
