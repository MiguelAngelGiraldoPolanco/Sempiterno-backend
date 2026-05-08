from datetime import datetime, timezone

from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Session, select


def create_user(db: Session, user_data: UserCreate) -> User:
    # if para asegurar que el cliente no exista en la base de datos
    if obtener_usuario_por_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="EL usuario ya existe")
    nuevo_user = User(**user_data.model_dump())
    db.add(nuevo_user)
    db.commit()
    db.refresh(nuevo_user)

    return nuevo_user


def obtener_usuario_por_id(db: Session, user_id: int):
    return db.get(User, user_id)


def obtener_usuario_por_email(db: Session, user_email: EmailStr):
    sentencia = select(User).where(User.email == user_email)
    resultados = db.exec(sentencia).firts()
    if not resultados:
        raise HTTPException(status_code=404, detail="EL usuario no existe.")
    return resultados


def modificar_usuario(db: Session, user_data: User):
    user_db = db.get(User, User.id)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    user_db.email = user_data.email
    user_db.password_hash = user_data.password_hash
    user_db.update_at = datetime.now(timezone.utc)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def eliminar_usuario(db: Session, user_id: int):
    user_db = obtener_usuario_por_id(db, user_id)
    db.delete(user_db)
    db.commit()
    return {"ok": True, "message": "Usuario eliminado"}
