from typing import Generator

from app.core.config import settings
from sqlmodel import Session, SQLModel, create_engine

# El motor: "check_same_thread" es necesario solo para SQLite
engine = create_engine(settings.DATABASE_URL, echo=True)


# Función para crear las tablas al iniciar la app
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# La "Dependencia" que usaremos en los endpoints
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
