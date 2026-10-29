# Schemas de TaskFlow (Práctica 1.2)
#
# Un schema es el contrato de la API: indica qué datos tiene que mandar el
# cliente (Create) y qué datos le devuelve el servidor (Read).
# No es lo mismo que el modelo de la base de datos. El modelo de BD es cómo se
# guardan los datos en las tablas, y el schema es lo que viaja en el JSON.
# Por ahora no se incluyen los usuarios, solo tareas y proyectos.

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------------- TAREAS ----------------

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
                    "title": "Hacer la práctica 1.2",
                    "description": "Crear los schemas con Pydantic",
                    "project_id": 1,
                }
            ]
        }
    )


# Datos que devuelve la API: los de TaskCreate + id, completed y created_at
class TaskRead(TaskBase):
    # from_attributes permite crear el schema a partir del modelo de la base de datos
    model_config = ConfigDict(from_attributes=True)

    id: int
    completed: bool = False
    created_at: datetime


# ---------------- PROYECTOS ----------------

# Campos comunes del proyecto
class ProjectBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


# Datos que manda el cliente para crear un proyecto
class ProjectCreate(ProjectBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Rediseño web",
                    "description": "Cambiar el diseño de la web",
                }
            ]
        }
    )


# Datos que devuelve la API: los de ProjectCreate + id y created_at
class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
