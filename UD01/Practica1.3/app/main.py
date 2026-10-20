from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import projects, tasks

app = FastAPI(title="TaskFlow API")


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
