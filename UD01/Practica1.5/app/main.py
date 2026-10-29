import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import models  # se importa para que SQLAlchemy conozca las tablas antes de crearlas
from app.database import Base, engine
from app.routers import projects, tasks

# Crea las tablas en taskflow.db si todavía no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")


# CORS: el navegador bloquea las peticiones que vienen de otra dirección.
# El frontend (Vue con Vite) irá en http://localhost:5173, así que le doy permiso
# a ese origen para que pueda llamar a la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Middleware propio: mide cuánto tarda la API en responder cada petición
# y lo añade en la cabecera X-Process-Time (en milisegundos).
# Se ejecuta en todas las peticiones, antes y después del endpoint.
# Si el endpoint lanza un error lo paso al handler global, así la respuesta
# 500 también lleva la cabecera.
@app.middleware("http")
async def tiempo_respuesta(request: Request, call_next):
    inicio = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        response = await error_general(request, exc)
    tiempo_ms = (time.perf_counter() - inicio) * 1000
    response.headers["X-Process-Time"] = f"{tiempo_ms:.2f}"
    return response


# Mensajes en español para los errores de validación
mensajes = {
    "missing": "Este campo es obligatorio",
    "string_too_short": "No puede estar vacío",
    "string_too_long": "No puede tener más de {max_length} caracteres",
    "int_parsing": "Tiene que ser un número",
    "greater_than": "Tiene que ser mayor que 0",
}


# Cambio el error 422 para que salga siempre igual y más claro
@app.exception_handler(RequestValidationError)
async def error_validacion(request: Request, exc: RequestValidationError):
    errores = []
    for error in exc.errors():
        campo = error["loc"][-1]
        mensaje = mensajes.get(error["type"], error["msg"])
        mensaje = mensaje.format(**error.get("ctx", {}))
        errores.append({"campo": campo, "mensaje": mensaje})
    return JSONResponse(status_code=422, content={"detail": errores})


# Handler global: si salta cualquier error que no hemos controlado,
# el servidor no se cae y el cliente recibe un 500 con un mensaje genérico,
# sin enseñar el stacktrace (que daría pistas de cómo está hecho el código).
@app.exception_handler(Exception)
async def error_general(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "Error interno del servidor"})


# Las rutas de tareas y proyectos están en la carpeta routers/
app.include_router(tasks.router)
app.include_router(projects.router)


# Rutas para comprobar que la API funciona (no son de negocio)
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "1.0.0"}


@app.get("/ping")
def ping():
    return {"message": "pong"}


# Ruta de prueba para forzar un error y comprobar el handler global
@app.get("/error")
def forzar_error():
    raise Exception("Error forzado para probar el handler")
