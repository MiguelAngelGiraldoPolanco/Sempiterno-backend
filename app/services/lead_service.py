from datetime import datetime, timezone
from typing import Sequence

from app.models.lead import Lead
from app.schemas.lead import LeadCreate

# ÑÑÑÑ
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import Session, select


def crear_lead(
    db: Session,
    lead_data: LeadCreate,
) -> Lead:
    # Evaluamos primero si el email existe para que no pueda acceder a muchos desceuntos con el mismo email
    if obtener_leads_por_email(db, lead_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El lead ya existe",
        )
    nuevo_lead = Lead(**lead_data.model_dump())
    db.add(nuevo_lead)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad, intente de nuevo",
        )

    db.refresh(nuevo_lead)

    return nuevo_lead


def obtener_todos_los_leads(
    db: Session,
) -> Sequence[Lead]:
    return db.exec(select(Lead)).all()


def obtener_leads_por_fecha(
    db: Session,
    init_date: datetime,
    last_date: datetime,
) -> Sequence[Lead]:

    if init_date > last_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin",
        )

    sentencia = select(Lead).where(
        Lead.create_at.between(asegurar_utc(init_date), asegurar_utc(last_date))
    )

    return db.exec(sentencia).all()


def obtener_leads_por_email(
    db: Session,
    email: EmailStr,
) -> Lead | None:
    sentencia = select(Lead).where(Lead.email == email)

    return db.exec(sentencia).first()


def asegurar_utc(
    dt: datetime,
) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
