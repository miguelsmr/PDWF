# Práctica 1.5 — Modelos SQLAlchemy y conexión a BD

**Alumno:** Miguel Luzón Prado

Partiendo de la práctica 1.4, ahora los datos se guardan de verdad en una base de datos SQLite (`taskflow.db`) usando SQLAlchemy.

- `app/database.py`: el `engine` (conexión a `taskflow.db`), `SessionLocal` para crear sesiones, la clase `Base` de los modelos y la dependencia `get_db()`, que abre una sesión por petición y la cierra en el `finally`.
- `app/models.py`: los modelos `User`, `Project`, `Category` y `Task` según el documento del proyecto. `Task` tiene clave foránea a `Project` y a `Category` (relaciones 1-N). `Project` no tiene `owner_id` porque todos los usuarios acceden a todos los proyectos.
- Los endpoints `POST /tasks` y `POST /projects` usan `Depends(get_db)` y guardan en la base de datos.
- En `main.py` se crean las tablas al arrancar con `Base.metadata.create_all`.

El archivo `taskflow.db` se crea solo al arrancar y no se sube a GitHub (está en el `.gitignore`).

## Estructura

```
Practica1.5/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── tasks.py
│       └── projects.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Cómo arrancarlo

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
