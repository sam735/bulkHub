from pydantic.main import BaseModel
from schemas import User
from fastapi import APIRouter, Depends, HTTPException
from db import get_user,insert_user_details
from .utils import check_password, generate_token,validate_facebook_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

class Token(BaseModel):
    token: str

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
            raise HTTPException(status_code=401, detail="Invalid user/password")
    except Exception as e:
        raise  HTTPException(status_code=500,detail=str(e))

@router.post('/facebook')
async def login_with_facebook(token:Token):
    try:
        f_user_details = validate_facebook_token(token.token)
        user_to_login = get_user({'fb_id':str(f_user_details.get('id'))})
        if not user_to_login:
            _id = insert_user_details(
                {   'fb_id': f_user_details.get('id'),
                    'email': f_user_details.get('email').lower()
                }
            )
            jwt,id = generate_token(
                {
                    "user_id": str(_id),
                }
            )
            return {"access_token": jwt, "token_type": "bearer", "refresh_token": ""}

        else:
            jwt,id = generate_token(
                {
                    "email": user_to_login[0].get('email'),
                    "user_id": str(user_to_login[0].get('_id')),
                    "role": user_to_login[0].get('role')
                }
            )
            return {"access_token": jwt, "token_type": "bearer", "refresh_token": ""}
    except Exception as e:
        raise  HTTPException(status_code=500,detail=str(e))