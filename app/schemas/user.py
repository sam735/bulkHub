from bson.objectid import ObjectId
from hashlib import sha256
from typing import Optional
from pydantic import BaseModel
from schemas.pyobjectId import PyObjectId
from schemas.address import Address

class User(BaseModel):
    firstName: str
    lastName:str
    username: str
    email: str
    password: str
    role: int = 1

    @property
    def hash_password(self):
        salt = str(ObjectId())
        return sha256(salt.encode() + self.password.encode()).hexdigest() + ':' + salt

class CreateUserResponse(BaseModel):
    id :Optional[str]
    message:str

class CreateAddress(BaseModel):
    address:Address
    is_default:bool
    phone:str

class GetAddress(BaseModel):
    id : str
    firstName: str
    lastName: str
    address:Address
    phone:Optional[str]
    is_default:Optional[bool] = False

class UpdateAddress(BaseModel):
    street:Optional[str]
    line_1: Optional[str]
    line_2: Optional[str]
    phone:Optional[str]
    is_default:Optional[bool] = None

class GetUser(BaseModel):
    firstName: str
    lastName:str
    username: str
    email: str

class UpdateUser(BaseModel):
    firstName: Optional[str]
    lastName:Optional[str]
    username: Optional[str]
    email: Optional[str]
    role: Optional[int]
