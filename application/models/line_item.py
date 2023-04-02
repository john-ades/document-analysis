from typing import Optional

from pydantic import BaseModel

from .price import Price


class LineItem(BaseModel):
    description: str
    quantity: Optional[int]
    price: Optional[Price]
