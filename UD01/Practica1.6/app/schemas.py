# Schemas de TaskFlow
#
# Un schema es el contrato de la API: indica qué datos tiene que mandar el
# cliente (Create / Update) y qué datos le devuelve el servidor (Read).
# No es lo mismo que el modelo de la base de datos (models.py): el modelo es cómo
# se guardan los datos en las tablas, y el schema es lo que viaja en el JSON.

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------------- TAREAS ----------------

# Campos comunes de la tarea
class TaskBase(BaseModel):
    # quita los espacios del principio y del final, asi "   " cuenta como vacío
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    # proyecto y categoría son opcionales (RF-13 del documento de TaskFlow)
    project_id: int | None = Field(default=None, gt=0)
    category_id: int | None = Field(default=None, gt=0)


# Datos que manda el cliente para crear una tarea
class TaskCreate(TaskBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Hacer la práctica 1.6",
                    "description": "CRUD completo de tareas",
                    "project_id": 1,
                    "category_id": 1,
                }
            ]
        }
    )


# Datos para editar una tarea (PUT): los mismos que al crear + completed
class TaskUpdate(TaskBase):
    completed: bool = False


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


# Datos para crear o editar un proyecto
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


# Datos que devuelve la API al listar proyectos
class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


# Detalle de un proyecto: sus datos + la lista de sus tareas
class ProjectDetail(ProjectRead):
    tasks: list[TaskRead] = []


# ---------------- CATEGORÍAS ----------------

# Campos comunes de la categoría (nombre y color, RF-20)
class CategoryBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    color: str = Field(min_length=1, max_length=20)


# Datos para crear o editar una categoría
class CategoryCreate(CategoryBase):
    model_config = ConfigDict(
        json_schema_extra={"examples": [{"name": "Urgente", "color": "#FF0000"}]}
    )


# Datos que devuelve la API al listar categorías
class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# Detalle de una categoría: sus datos + la lista de sus tareas
class CategoryDetail(CategoryRead):
    tasks: list[TaskRead] = []
