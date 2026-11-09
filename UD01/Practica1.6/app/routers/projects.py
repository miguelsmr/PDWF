from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectDetail, ProjectRead

# Todas las rutas de este archivo empiezan por /projects y salen en el grupo "projects"
router = APIRouter(prefix="/projects", tags=["projects"])


# Busca un proyecto por id; si no existe devuelve 404
def buscar_proyecto(project_id: int, db: Session):
    proyecto = db.query(Project).filter(Project.id == project_id).first()
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto


# Listar todos los proyectos
@router.get("", response_model=list[ProjectRead])
def listar_proyectos(db: Session = Depends(get_db)):
    return db.query(Project).all()


# Detalle de un proyecto con sus tareas asociadas
@router.get("/{project_id}", response_model=ProjectDetail)
def obtener_proyecto(project_id: int, db: Session = Depends(get_db)):
    return buscar_proyecto(project_id, db)


# Crear un proyecto
@router.post("", response_model=ProjectRead, status_code=201)
def crear_proyecto(project: ProjectCreate, db: Session = Depends(get_db)):
    nuevo = Project(name=project.name, description=project.description)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# Editar el nombre y la descripción de un proyecto
@router.put("/{project_id}", response_model=ProjectRead)
def editar_proyecto(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    proyecto = buscar_proyecto(project_id, db)
    proyecto.name = project.name
    proyecto.description = project.description
    db.commit()
    db.refresh(proyecto)
    return proyecto


# Eliminar un proyecto: por el cascade del modelo se borran también sus tareas
@router.delete("/{project_id}", status_code=204)
def eliminar_proyecto(project_id: int, db: Session = Depends(get_db)):
    proyecto = buscar_proyecto(project_id, db)
    db.delete(proyecto)
    db.commit()
