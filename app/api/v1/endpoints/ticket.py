from typing import List

from app.schemas.tikets import ProductoItem, Ticket
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=List[Ticket])
def read_tikets():
    return [
        Ticket(
            id=57,
            customerName="Miguel Angel",
            products=[
                ProductoItem(nombre="Vela 1", cantidad=3, precio_unidad=129.0),
                ProductoItem(nombre="Vela 2", cantidad=5, precio_unidad=130.0),
            ],
            total=1037.0,
            iva=0.12,
        )
    ]


@router.get("/{tiket_id}")
async def read_tiket(item_id):
    return {"item_id": item_id}
