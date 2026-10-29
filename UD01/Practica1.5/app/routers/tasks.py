from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead

# Todas las rutas de este archivo empiezan por /tasks y salen en el grupo "tasks"
router = APIRouter(prefix="/tasks", tags=["tasks"])


# Crea la tarea y la guarda en la base de datos
@router.post("", response_model=TaskRead, status_code=201)
def crear_tarea(task: TaskCreate, db: Session = Depends(get_db)):
    nueva = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)  # recarga la tarea para tener el id y la fecha que pone la BD
    return nueva
