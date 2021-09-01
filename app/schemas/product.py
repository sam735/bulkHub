from typing import Optional, List
from pydantic import BaseModel

class CreateProduct(BaseModel):
    product_name:str
    product_category_id:str
    max_available_quantity_in_kg:float
    Price_per_kg:float

class DispalyProduct(BaseModel):
    id:str
    product_name: str
    product_image_url:Optional[str]
    max_available_quantity_in_kg:float
    Price_per_kg:float
    createdAt:str

class ProductList(BaseModel):
    items:List[DispalyProduct]

class UpdateProduct(BaseModel):
    max_available_quantity_in_kg:Optional[float]
    Price_per_kg:Optional[float]