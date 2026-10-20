# Configuración general de la API, así no hay valores sueltos por el código

NOMBRE_APP = "TaskFlow API"
VERSION = "1.0.0"

# Todas las rutas de negocio van con este prefijo
API_PREFIX = "/api/v1"

# Descripción de cada grupo (tag) que sale en Swagger
TAGS = [
    {"name": "tasks", "description": "Gestión de las tareas."},
    {"name": "projects", "description": "Gestión de proyectos, que sirven para agrupar las tareas."},
    {"name": "health", "description": "Comprobar que la API está funcionando."},
]
