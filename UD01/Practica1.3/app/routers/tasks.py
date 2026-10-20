from datetime import datetime

from fastapi import APIRouter

from app.schemas import TaskCreate, TaskRead

# Todas las rutas de este archivo empiezan por /tasks y salen en el grupo "tasks"
router = APIRouter(prefix="/tasks", tags=["tasks"])


# POST temporal: como aún no hay base de datos devuelvo una tarea simulada
@router.post("", response_model=TaskRead, status_code=201, summary="Crear una tarea")
def crear_tarea(task: TaskCreate):
    return TaskRead(
        id=1,
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        completed=False,
        created_at=datetime.now(),
    )
