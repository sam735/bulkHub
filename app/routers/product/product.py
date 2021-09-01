from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from routers.user.utils import is_seller
from bson.objectid import ObjectId
from schemas.product import CreateProduct,DispalyProduct,ProductList,UpdateProduct
from db import insert_product,get_product,get_each_product_category,update_product,delete_product

router = APIRouter()

@router.post('/')
async def create_product(product:CreateProduct,current_user=Depends(is_seller)):
    try:
        db_product = {
            'product_name':product.product_name,
            'product_category_id':product.product_category_id,
            'seller_id':current_user.get('id'),
            'max_available_quantity_in_kg':product.max_available_quantity_in_kg,
            'Price_per_kg':product.Price_per_kg
        }
        id = insert_product(db_product)
        return {'message':'product created successfully','id':str(id)}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.get('/',response_model=ProductList)
async def list_product(current_user=Depends(is_seller)):
    try:
        products = get_product({'seller_id':current_user.get('id')})
        product_image_mapper={}
        product_to_list = []
        for product in products:
            if product_image_mapper.get(product.get('product_name')) == None:
                product_category_detals = get_each_product_category(
                    {
                        'productName':product.get('product_name')
                    }
                )
                product_image_mapper[product.get('product_name')] = product_category_detals[0].get('productImageURL')
            product_to_list.append(DispalyProduct(
                id = str(product.get('_id')),
                product_name = product.get('product_name'),
                product_image_url = product_image_mapper.get(product.get('product_name')),
                max_available_quantity_in_kg = product.get('max_available_quantity_in_kg'),
                Price_per_kg = product.get('Price_per_kg'),
                createdAt = str(product.get('createdAt'))
            ))
        return ProductList(items = product_to_list)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.patch('/{product_id}')
async def update_product_details(product_id:str,update_details:UpdateProduct,
    current_user=Depends(is_seller)):
    try:
        update_product({'_id':ObjectId(product_id),'seller_id':current_user.get('id')},dict(update_details))
        return {'message':'product details uploaded successfully'}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.delete('/{product_id}')
async def remove_product(product_id:str,current_user=Depends(is_seller)):
    try:
        id = delete_product({'_id':ObjectId(product_id),'seller_id':current_user.get('id')})
        if id:
            return {"message":"product removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))