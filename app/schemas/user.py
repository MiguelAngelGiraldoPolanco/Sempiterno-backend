from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password_hash: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None


class UserLogin(BaseModel):
    id: int
    access_token: str
    token_type: str


class UserRead(UserBase):
    id: int
    create_at: datetime
    update_at: datetime
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)
