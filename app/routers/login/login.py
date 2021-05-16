from schemas import User
from fastapi import APIRouter, Depends, HTTPException
from db import get_user
from .utils import check_password, generate_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post('/')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user_to_login = get_user({'email':form_data.username})
        if user_to_login and check_password(form_data.password, user_to_login[0].get('hashPassword')):
            jwt,id = generate_token(
                {
                    "email": user_to_login[0].get('email'),
                    "user_id": str(user_to_login[0].get('_id')),
                    "role": user_to_login[0].get('role')
                }
            )
            return {"access_token": jwt, "token_type": "bearer", "refresh_token": ""}
        else:
            raise Exception('Invalid password or user name')
    except Exception as e:
        raise  HTTPException(status_code=500,detail=str(e))