from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryDetail, CategoryRead

# Todas las rutas de este archivo empiezan por /categories y salen en el grupo "categories"
router = APIRouter(prefix="/categories", tags=["categories"])


# Busca una categoría por id; si no existe devuelve 404
def buscar_categoria(category_id: int, db: Session):
    categoria = db.query(Category).filter(Category.id == category_id).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


# Listar todas las categorías
@router.get("", response_model=list[CategoryRead])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Category).all()


# Detalle de una categoría con sus tareas asociadas
@router.get("/{category_id}", response_model=CategoryDetail)
def obtener_categoria(category_id: int, db: Session = Depends(get_db)):
    return buscar_categoria(category_id, db)


# Crear una categoría
@router.post("", response_model=CategoryRead, status_code=201)
def crear_categoria(category: CategoryCreate, db: Session = Depends(get_db)):
    nueva = Category(name=category.name, color=category.color)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# Editar el nombre y el color de una categoría
@router.put("/{category_id}", response_model=CategoryRead)
def editar_categoria(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    categoria = buscar_categoria(category_id, db)
    categoria.name = category.name
    categoria.color = category.color
    db.commit()
    db.refresh(categoria)
    return categoria


# Eliminar una categoría: por el cascade del modelo se borran también sus tareas
@router.delete("/{category_id}", status_code=204)
def eliminar_categoria(category_id: int, db: Session = Depends(get_db)):
    categoria = buscar_categoria(category_id, db)
    db.delete(categoria)
    db.commit()
