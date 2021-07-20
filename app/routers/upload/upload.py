from fastapi import APIRouter, Depends, HTTPException,File, UploadFile
from .utils import upload_to_aws
from constant import image_url
from bson.objectid import ObjectId
from routers.user.utils import get_current_user
# from PIL import Image
# import io

router = APIRouter()

@router.post('/')
async def upload_image(file: UploadFile = File(...),current_user = Depends(get_current_user)):
    try:
        id = str(ObjectId())
        file_details = file.filename.split('.')
        image = file.file
        file_name = "{}-{}.{}".format(str(id),file_details[0],file_details[1])
        uplod_status = upload_to_aws(image,'bulkhub-image',file_name)
        if uplod_status:
            return {'image_url':image_url.format(file_name)}
        else:
            raise HTTPException(status_code=500,detail=str("something went wrong try after some time"))
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))