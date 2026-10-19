from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas import TaskCreate, TaskRead

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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "1.0.0"}


@app.get("/ping")
def ping():
    return {"message": "pong"}


# POST temporal: como aún no hay base de datos devuelvo una tarea simulada
@app.post("/tasks", response_model=TaskRead, status_code=201)
def crear_tarea(task: TaskCreate):
    return TaskRead(
        id=1,
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        completed=False,
        created_at=datetime.now(),
    )
