# Schemas de las tareas: lo que manda el cliente (Create) y lo que devuelve la API (Read)

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# Campos comunes de la tarea, los usan TaskCreate y TaskRead
class TaskBase(BaseModel):
    # quita los espacios del principio y del final, asi "   " cuenta como vacío
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    project_id: int = Field(gt=0)


# Datos que manda el cliente para crear una tarea
class TaskCreate(TaskBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Hacer la práctica 1.3",
                    "description": "Separar las rutas con APIRouter",
                    "project_id": 1,
                }
            ]
        }
    )


# Datos que devuelve la API: los de TaskCreate + id, completed y created_at
class TaskRead(TaskBase):
    id: int
    completed: bool = False
    created_at: datetime
