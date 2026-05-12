from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# 1. El objeto que representa cada producto en el JSON
class LeadBase(BaseModel):
    email: EmailStr
    marketing_consent: Optional[bool] = False


class LeadCreate(LeadBase):
    pass


class LeadRead(LeadBase):
    id: int
    create_at: datetime
    marketing_consent: bool

    class Config:
        # Esto es vital para que Pydantic pueda leer
        # los datos desde SQLModel/Base de datos
        from_attributes = True
