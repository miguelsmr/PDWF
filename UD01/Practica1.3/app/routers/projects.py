from datetime import datetime

from fastapi import APIRouter

from app.schemas import ProjectCreate, ProjectRead

# Todas las rutas de este archivo empiezan por /projects y salen en el grupo "projects"
router = APIRouter(prefix="/projects", tags=["projects"])


# POST temporal, igual que el de tareas, devuelve un proyecto simulado
@router.post("", response_model=ProjectRead, status_code=201, summary="Crear un proyecto")
def crear_proyecto(project: ProjectCreate):
    return ProjectRead(
        id=1,
        name=project.name,
        description=project.description,
        created_at=datetime.now(),
    )
