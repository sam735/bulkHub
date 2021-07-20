from .address import Address
from typing import Optional, List
from pydantic import BaseModel


class ProductcategoryAddition(BaseModel):
    productName: str
    productType: str
    productImageURL: Optional[str]

class GetProductcategory(BaseModel):
    productName: str
    productType: str
    productImageURL: Optional[str]
    createdAt: Optional[str]

class GetProductCategoryList(BaseModel):
    items: List[GetProductcategory]
    id: str

class UpdateProductCategory(BaseModel):
    productName: Optional[str]
    productType: Optional[str]

class DeleteProductCategory(BaseModel):
    productName: Optional[str]
    productType: Optional[str]