# Modelos de la base de datos: cada clase es una tabla y cada atributo una columna.
# Están hechos según el documento de TaskFlow. No hay owner_id en Project porque
# todos los usuarios pueden acceder a todos los proyectos.

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # Un proyecto tiene muchas tareas (relación 1-N)
    tasks = relationship("Task", back_populates="project")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)

    # Una categoría tiene muchas tareas (relación 1-N)
    tasks = relationship("Task", back_populates="category")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    # Claves foráneas: la tarea puede pertenecer a un proyecto y a una categoría (opcional)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    project = relationship("Project", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
