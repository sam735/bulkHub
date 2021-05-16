import enum

from pymongo import message
from schemas import User,CreateUserResponse
from fastapi import APIRouter, Depends, HTTPException
from db import get_db,get_user,insert_user_details

router = APIRouter()

class Role(enum.Enum):
    buyer=1
    seller=2

@router.post('/',response_model=CreateUserResponse)
async def create_user(user: User):
        try:
            user_details = get_user({'email':user.email.lower()})
            if user_details:
                return CreateUserResponse(id = str(user_details[0].get('_id')),
                                        message = 'user with email {} alrady exist'.format(user.email)
                                    )
            else:
                _id = insert_user_details(
                    {   'firstName':user.firstName,
                        'lastName':user.lastName,
                        'username':user.username,
                        'email':user.email.lower(),
                        'hashPassword':user.hash_password,
                        'role':Role(user.role).name
                    }
                )
                return CreateUserResponse(id=str(_id),message='User created successfully')
        except Exception as e:
            raise  HTTPException(status_code=500,detail=str(e))