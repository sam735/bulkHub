from schemas.cart import CartItems,UpdateCart,GetCart,GetCartItems
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from routers.user.utils import is_buyer
from bson.objectid import ObjectId
from db import insert_cart_items,get_user_cart,update_cart_items

router = APIRouter()

@router.post('/')
async def add_items_to_cart(cart_items:CartItems,current_user=Depends(is_buyer)):
    try:
        user_cart_items=get_user_cart({'user_id':current_user.get('id')})
        if user_cart_items:
            update_cart_items(
                {'user_id':current_user.get('id')},
                {
                    '$push':{
                        'products':{
                            '$each':[dict(item) for item in cart_items.items]
                        }
                    },
                    '$set':{'updatedAt':datetime.now()}
                }
            )
        else:
            id = insert_cart_items(
                {
                    'user_id':current_user.get('id'),
                    'products':[dict(item) for item in cart_items.items]
                }
            )
        return {"message":"Items added successfully to the cart"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch('/')
async def update_cart_item(update_item:UpdateCart,current_user=Depends(is_buyer)):
    try:
        update_cart_items(
            {
                'user_id':current_user.get('id'),
                'products':{
                    '$elemMatch': {
                        'product_name':update_item.product_name
                    }
                }
            },
            {
                '$set':{
                    'products.$.quantity_in_kg':update_item.quantity_in_kg,
                    'updatedAt':datetime.now()
                }
            }
        )
        return {"message":"cart updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/')
async def delete_cart_item(product_name:str,current_user=Depends(is_buyer)):
    try:
        update_cart_items(
            {'user_id':current_user.get('id')},
            {
                '$pull':{
                    'products':{
                        'product_name':product_name
                    }
                },
                '$set':{'updatedAt':datetime.now()}
            },
        )
        return {"message":"removed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/',response_model=GetCart)
async def get_cart_items(current_user=Depends(is_buyer)):
    try:
        user_cart_items=get_user_cart({'user_id':current_user.get('id')})
        items = []
        if user_cart_items:
            items = [GetCartItems(
                product_name = item.get('product_name'),
                quantity_in_kg=item.get('quantity_in_kg'),
                price_per_kg_in_rs=item.get('price_per_kg_in_rs'),
                created_at=str(user_cart_items[0].get('createdAt'))
            ) for item in user_cart_items[0].get('products')] 
        return GetCart(items=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))