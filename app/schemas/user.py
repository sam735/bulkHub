from bson.objectid import ObjectId
from hashlib import sha256
from typing import Optional
from pydantic import BaseModel
# from app.schemas import PyObjectId

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