from schemas.address import Address
from bson.objectid import ObjectId
from schemas.user import CreateUserResponse
from fastapi import APIRouter, Depends, HTTPException
from routers.user.utils import is_seller
from schemas.seller import SellerRegistration,UpdateSellerAddress,GetSeller
from db import create_seller,get_seller,create_seller_address,update_seller_address,get_seller_address
from datetime import datetime

router = APIRouter()

@router.post('/',response_model=CreateUserResponse)
async def register_seller(seller_details:SellerRegistration,current_user = Depends(is_seller)):

    seller = get_seller({'phoneNo':seller_details.phoneNo})
    if seller:
        raise HTTPException(status_code=422,detail='there is seller associated with this phone no')
    try:
        seller_details = dict(seller_details)
        seller_details['userId'] = current_user.get('id')
        seller_details['createdAt'] = datetime.now()
        seller = create_seller(seller_details)
        return CreateUserResponse(id = str(seller),message='seller created successfully')
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.post('/address')
async def link_address(seller_adress:Address,current_user = Depends(is_seller)):
    try:
        seller = get_seller({'userId':current_user.get('id')})
        seller_adress = dict(seller_adress)
        seller_adress['seller_id'] = str(seller[0]['_id'])
        create_seller_address(seller_adress)
        return {'message':'seller address created'}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.patch('/address')
async def edit_address(address_to_update:UpdateSellerAddress,current_user = Depends(is_seller)):
    try:
        seller = get_seller({'userId':current_user.get('id')})
        address_to_update = dict(address_to_update)
        address_to_update = {k:v for k,v in address_to_update.items() if v is not None }
        update_seller_address({'seller_id':str(seller[0].get('_id'))},address_to_update)
        return {'Message':'Address updated'}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.get('/',response_model=GetSeller)
def seller_details(current_user = Depends(is_seller)):
    try:
        seller = get_seller({'userId':current_user.get('id')})[0]
        seller_address = get_seller_address({'seller_id':str(seller.get('_id'))})
        address = None
        if seller_address:
            address = Address(
                street = seller_address[0].get('street'),
                line_1 = seller_address[0].get('line_1'),
                line_2 = seller_address[0].get('line_2'),
                city = seller_address[0].get('city'),
                state = seller_address[0].get('state'),
                zip = seller_address[0].get('zip'),
                country = seller_address[0].get('country')
        )
        return GetSeller(sellerName = seller.get('sellerName'),BusinessName = seller.get('BusinessName'),
            phoneNo = seller.get('phoneNo'), address = address
        )
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))