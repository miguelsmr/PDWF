# Schemas de los proyectos

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


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
    id: int
    created_at: datetime
