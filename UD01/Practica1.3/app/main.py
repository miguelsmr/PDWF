from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.config import API_PREFIX, NOMBRE_APP, TAGS, VERSION
from app.core.errores import error_validacion
from app.routers import health, projects, tasks

# main.py solo crea la app y la configura, las rutas están en la carpeta routers/
app = FastAPI(title=NOMBRE_APP, version=VERSION, openapi_tags=TAGS)

app.add_exception_handler(RequestValidationError, error_validacion)

# Rutas de negocio con el prefijo de la versión: /api/v1/tasks y /api/v1/projects
app.include_router(tasks.router, prefix=API_PREFIX)
app.include_router(projects.router, prefix=API_PREFIX)

# Las de comprobación van sin prefijo: /health, /version y /ping
app.include_router(health.router)
