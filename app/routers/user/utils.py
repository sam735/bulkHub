from fastapi import Depends,HTTPException,status
from routers.login.utils import verify_decode_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = verify_decode_token(token)["data"]
    user_id = user_data["user_id"]
    roles = user_data['role']
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {'id':user_id, 'role':roles}

async def is_seller(current_user = Depends(get_current_user)):
    if current_user.get('role') != 'seller':
        raise HTTPException(
            status_code=403,
            detail="Invalid roles user need to be register as seller first",
        )
    return current_user