from datetime import datetime
from typing import List, Optional

from sqlmodel import JSON, Column, Field, SQLModel


class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customerName: str
    products: List[dict] = Field(default=[], sa_column=Column(JSON))
    date: datetime = Field(default_factory=datetime.now)
    total: float
    iva: float = 0.0
