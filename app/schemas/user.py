from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_admin: bool


class UserCreate(UserBase):
    password_hash: str


class UserRead(UserBase):
    id: int
    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True
