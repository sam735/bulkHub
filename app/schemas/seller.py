from .address import Address
from typing import Optional
from pydantic import BaseModel

class SellerRegistration(BaseModel):
    sellerName: str
    BusinessName :str
    phoneNo:str

class UpdateSellerAddress(BaseModel):
    street:Optional[str]
    line_1: Optional[str]
    line_2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[int]

class GetSeller(BaseModel):
    sellerName: str
    BusinessName :str
    phoneNo:str
    address:Address