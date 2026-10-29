from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectRead

# Todas las rutas de este archivo empiezan por /projects y salen en el grupo "projects"
router = APIRouter(prefix="/projects", tags=["projects"])


# Crea el proyecto y lo guarda en la base de datos
@router.post("", response_model=ProjectRead, status_code=201)
def crear_proyecto(project: ProjectCreate, db: Session = Depends(get_db)):
    nuevo = Project(name=project.name, description=project.description)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
