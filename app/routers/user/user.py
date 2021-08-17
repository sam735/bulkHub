import enum
from typing import List
from bson.objectid import ObjectId
from datetime import datetime
from schemas import (User,CreateUserResponse,CreateAddress,GetAddress,Address,UpdateAddress,
                GetUser,UpdateUser
)
from fastapi import APIRouter, Depends, HTTPException
from db import (get_user,insert_user_details,create_address,get_address,update_address,
                delete_address,update_user_detail
)
from .utils import get_current_user

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
                    {   
                        'email':user.email.lower(),
                        'hashPassword':user.hash_password,
                        'role':Role(user.role).name
                    }
                )
                return CreateUserResponse(id=str(_id),message='User created successfully')
        except Exception as e:
            raise  HTTPException(status_code=500,detail=str(e))

@router.get('/',response_model=GetUser)
async def get_user_details(current_user = Depends(get_current_user)):
    try:
        user_details = get_user({'_id':ObjectId(current_user.get('id'))})[0]
        return GetUser(
            firstName = user_details.get('firstName'),
            lastName = user_details.get('lastName'),
            username = user_details.get('username'),
            email = user_details.get('email'),
            image_url = user_details.get('image_url')
        )
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.patch('/',response_model=CreateUserResponse)
async def update_user_details(user_details:UpdateUser,current_user = Depends(get_current_user)):
    try:
        update_dict = {k:v for k,v in dict(user_details).items() if v is not None}
        if update_dict.get('role'):
            update_dict['role'] = Role(user_details.role).name
        update_user_detail({'_id':ObjectId(current_user.get('id'))},update_dict)
        return CreateUserResponse(id=str(current_user.get('id')),message='User details updated')
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.post('/address',response_model=CreateUserResponse)
async def add_address(user_address:CreateAddress, current_user = Depends(get_current_user)):
    try:
        if user_address.is_default:
            update_address({},{'is_default':False})
        address_payload = {
            'user_id': current_user.get('id'),
            'user_address':dict(user_address.address),
            'is_default': user_address.is_default
        }
        id = create_address(address_payload)
        return CreateUserResponse(id=str(id),message='address added successfully')
    except Exception as e:
        raise  HTTPException(status_code=500,detail=str(e))

@router.get('/address',response_model=List[GetAddress])
async def get_user_address(current_user = Depends(get_current_user)):
    try:
        user_detils = get_user({'_id':ObjectId(current_user.get('id'))})
        user_address = get_address({'user_id':current_user.get('id')})
        if user_address:
            data = [GetAddress(
                id = str(address.get('_id')),
                firstName = user_detils[0].get('firstName'),
                lastName = user_detils[0].get('lastName'),
                address = Address(
                    street = address.get('user_address').get('street'),
                    line_1 = address.get('user_address').get('line_1'),
                    line_2 = address.get('user_address').get('line_2'),
                    city = address.get('user_address').get('city'),
                    state = address.get('user_address').get('state'),
                    zip = address.get('user_address').get('zip'),
                    country = address.get('user_address').get('country')
                ),
                phone = address.get('phone'),
                is_default=address.get('is_default')
            ) for address in user_address]
            return data
        else:
            raise HTTPException(status_code=404, detail="No address found")
    except Exception as e:
        raise  HTTPException(status_code=500,detail=str(e))

@router.patch('/address/{address_id}')
async def update_user_address(address_id:str,address_to_update:UpdateAddress, current_user = Depends(get_current_user)):
    try:
        if address_to_update.is_default:
            update_address({},{'is_default':False})
        address = dict(address_to_update)
        if address_to_update.is_default is None:
            address.pop('is_default')
        if address_to_update.is_default is False and get_address({'_id':ObjectId(address_id),'is_default':True}):
            return {'message':'before making it not default first choose other address as default'}
        update_address({'_id':ObjectId(address_id)},address)
        return {'message':'address updated successfully'}
    except Exception as e:
        raise  HTTPException(status_code=500,detail=str(e))

@router.delete('/address/{address_id}')
async def delete_user_address(address_id:str,current_user = Depends(get_current_user)):
    try:
        delete_address({'_id':ObjectId(address_id)})
        return {'message':'address removed successfully'}
    except Exception as e:
        raise  HTTPException(status_code=500,detail=str(e))

