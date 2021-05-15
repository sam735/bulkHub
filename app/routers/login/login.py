from fastapi import APIRouter, Depends, HTTPException
from db import get_db

router = APIRouter()

@router.post('/')
async def login(db = Depends(get_db)):
    try:
        return {"message":'welcome to login'}
    except Exception as e:
        raise  HTTPException(status_code=500,detail=str(e))