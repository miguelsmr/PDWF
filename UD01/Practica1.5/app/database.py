from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Dirección de la base de datos: un archivo SQLite llamado taskflow.db en la carpeta del proyecto
DATABASE_URL = "sqlite:///./taskflow.db"

# El engine es la conexión con la base de datos.
# check_same_thread=False hace falta en SQLite porque FastAPI puede atender
# una petición en un hilo distinto al que abrió la conexión.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Fábrica de sesiones: cada vez que llamo a SessionLocal() tengo una sesión nueva
# para hablar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredan todos los modelos (forma declarative)
Base = declarative_base()


# Dependencia para los endpoints: abre una sesión por petición
# y la cierra siempre al terminar, aunque haya un error (finally)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
