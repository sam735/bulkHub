from typing import List, Optional
from pydantic import BaseModel

class CreateCart(BaseModel):
    product_name:str
    quantity_in_kg:float
    price_per_kg_in_rs:float

class CartItems(BaseModel):
    items: List[CreateCart]

class UpdateCart(BaseModel):
    product_name:str
    quantity_in_kg:float

class GetCartItems(BaseModel):
    product_name:str
    quantity_in_kg:float
    price_per_kg_in_rs:float
    created_at:str

class GetCart(BaseModel):
    items:List[GetCartItems]