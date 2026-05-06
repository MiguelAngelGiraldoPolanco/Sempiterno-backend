from typing import Generator

from sqlmodel import Session, SQLModel, create_engine, text

# Nombre del archivo que se creará en tu contenedor Docker
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# El motor: "check_same_thread" es necesario solo para SQLite
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


# Función para crear las tablas al iniciar la app
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# La "Dependencia" que usaremos en los endpoints
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def set_initial_id():
    with Session(engine) as session:
        # empieza el conteo en la factura 57
        session.exec(
            text(
                "INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES ('ticket', 57)"
            )
        )
        session.commit()
