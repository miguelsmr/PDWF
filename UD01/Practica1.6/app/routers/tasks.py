from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category, Project, Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate

# Todas las rutas de este archivo empiezan por /tasks y salen en el grupo "tasks"
router = APIRouter(prefix="/tasks", tags=["tasks"])


# Busca una tarea por id; si no existe devuelve 404
def buscar_tarea(task_id: int, db: Session):
    tarea = db.query(Task).filter(Task.id == task_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


# Comprueba que el proyecto y la categoría que se indican existen
def comprobar_relaciones(task: TaskCreate, db: Session):
    if task.project_id is not None:
        if db.query(Project).filter(Project.id == task.project_id).first() is None:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    if task.category_id is not None:
        if db.query(Category).filter(Category.id == task.category_id).first() is None:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")


# Listar tareas con filtros opcionales (project_id, completed) y paginación (skip, limit)
@router.get("", response_model=list[TaskRead])
def listar_tareas(
    project_id: int | None = None,
    completed: bool | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    consulta = db.query(Task)
    if project_id is not None:
        consulta = consulta.filter(Task.project_id == project_id)
    if completed is not None:
        consulta = consulta.filter(Task.completed == completed)
    # skip = cuántas se salta, limit = cuántas devuelve como máximo
    return consulta.offset(skip).limit(limit).all()


# Detalle de una tarea
@router.get("/{task_id}", response_model=TaskRead)
def obtener_tarea(task_id: int, db: Session = Depends(get_db)):
    return buscar_tarea(task_id, db)


# Crear una tarea
@router.post("", response_model=TaskRead, status_code=201)
def crear_tarea(task: TaskCreate, db: Session = Depends(get_db)):
    comprobar_relaciones(task, db)
    nueva = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        category_id=task.category_id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)  # recarga la tarea para tener el id y la fecha que pone la BD
    return nueva


# Editar una tarea (se mandan todos los campos)
@router.put("/{task_id}", response_model=TaskRead)
def editar_tarea(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    tarea = buscar_tarea(task_id, db)
    comprobar_relaciones(task, db)
    tarea.title = task.title
    tarea.description = task.description
    tarea.project_id = task.project_id
    tarea.category_id = task.category_id
    tarea.completed = task.completed
    db.commit()
    db.refresh(tarea)
    return tarea


# Eliminar una tarea (204 = borrado correctamente, sin contenido en la respuesta)
@router.delete("/{task_id}", status_code=204)
def eliminar_tarea(task_id: int, db: Session = Depends(get_db)):
    tarea = buscar_tarea(task_id, db)
    db.delete(tarea)
    db.commit()
