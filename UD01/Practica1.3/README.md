# Práctica 1.3 — Organización con APIRouter

**Alumno:** Miguel Luzón Prado

Las rutas de tareas y proyectos ya no están en `main.py`, cada recurso tiene su archivo en `app/routers/` con un `APIRouter` con su `prefix` y sus `tags`. En `main.py` se incluyen con `app.include_router(...)`.

## Estructura

```
Practica1.3/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── tasks.py
│       └── projects.py
├── capturas/
├── README.md
└── requirements.txt
```

## Endpoints

- `POST /tasks` → crea una tarea (simulada), grupo `tasks`
- `POST /projects` → crea un proyecto (simulado), grupo `projects`
- `GET /health`, `GET /version`, `GET /ping` → comprobar que la API funciona

Separar las rutas por recurso hace que cada archivo sea más corto y que sea más fácil encontrar y cambiar las cosas cuando la API vaya creciendo.

## Cómo arrancarlo

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
