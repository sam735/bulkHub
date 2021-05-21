from bson.objectid import ObjectId
from typing import Optional
from pydantic import BaseModel

class Address(BaseModel):
    street:str
    line_1: str
    line_2: Optional[str]
    city: str
    state: str
    zip: int
    country: str