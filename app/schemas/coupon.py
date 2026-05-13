from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CouponBase(BaseModel):
    name: str
    finish_at: datetime
    discount: float


class CouponCreate(CouponBase):
    pass


class CouponRead(CouponBase):
    id: int
    create_at: datetime

    model_config = ConfigDict(from_attributes=True)
