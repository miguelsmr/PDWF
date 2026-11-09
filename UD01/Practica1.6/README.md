# Práctica 1.6 — CRUD completo

**Alumno:** Miguel Luzón Prado

Partiendo de la práctica 1.5, ahora tasks, projects y categories tienen las 5 operaciones CRUD sobre la base de datos (crear, listar, ver detalle, editar y eliminar).

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | /tasks | Lista tareas (filtros: `project_id`, `completed`; paginación: `skip`, `limit`) |
| GET | /tasks/{id} | Detalle de una tarea |
| POST | /tasks | Crea una tarea |
| PUT | /tasks/{id} | Edita una tarea |
| DELETE | /tasks/{id} | Elimina una tarea |
| GET | /projects | Lista proyectos |
| GET | /projects/{id} | Detalle de proyecto (con sus tareas) |
| POST | /projects | Crea un proyecto |
| PUT | /projects/{id} | Edita un proyecto |
| DELETE | /projects/{id} | Elimina un proyecto |
| GET | /categories | Lista categorías |
| GET | /categories/{id} | Detalle de categoría (con sus tareas) |
| POST | /categories | Crea una categoría |
| PUT | /categories/{id} | Edita una categoría |
| DELETE | /categories/{id} | Elimina una categoría |

Si se pide algo que no existe (una tarea, proyecto o categoría con un id que no está) la API devuelve **404** con un mensaje. Al crear o editar una tarea también se comprueba que el proyecto y la categoría indicados existen.

## Qué pasa al borrar un proyecto o una categoría

He elegido **borrado en cascada**: al eliminar un proyecto se eliminan también sus tareas, y lo mismo con las categorías. Está puesto en `models.py` con `cascade="all, delete"` en las relaciones.

Lo he decidido así porque las tareas pertenecen a su proyecto: si el proyecto desaparece, sus tareas se quedarían apuntando a un id que ya no existe (huérfanas). Con la cascada no quedan datos sueltos en la base de datos, y se hace igual en proyectos y categorías para que el sistema sea consistente.

## Colección de Postman

En `postman/TaskFlow-Practica1.6.postman_collection.json` están las 15 peticiones, numeradas en el orden en que hay que ejecutarlas (primero se crean proyecto y categoría, luego la tarea, y al final se borra todo). La dirección de la API está en la variable `base_url` (`http://127.0.0.1:8000`).

## Estructura

```
Practica1.6/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── tasks.py
│       ├── projects.py
│       └── categories.py
├── postman/
│   └── TaskFlow-Practica1.6.postman_collection.json
├── .gitignore
├── README.md
└── requirements.txt
```

## Cómo arrancarlo

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
