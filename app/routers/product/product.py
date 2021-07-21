from fastapi import APIRouter, Depends, HTTPException
from routers.user.utils import is_seller
from schemas.product import ProductcategoryAddition, GetProductcategory, GetProductCategoryList, UpdateProductCategory
from db import create_product_category_type, get_product_category, update_product_category, get_each_product_category, delete_product_category
from datetime import datetime
from bson.objectid import ObjectId

router = APIRouter()


@router.post('/')
async def create_product_category(product_details: ProductcategoryAddition, current_user=Depends(is_seller)):
    try:
        create_product_category_type({'productName': product_details.productName,
                                      'productType': product_details.productType,
                                      'createdAt': datetime.now(),
                                      'productImageURL': product_details.productImageURL})
        return {'message': 'product category created',
                'id': str(id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/', response_model=GetProductCategoryList)
async def list_product_category(current_user=Depends(is_seller)):
    try:
        product_category = get_product_category()
        product_items = [GetProductcategory(productName=item.get('productName'),
                                            productType=item.get('productType'),
                                            productImageURL=item.get('productImageURL'),
                                            createdAt=str(item.get('createdAt'))) for item in product_category]
        return GetProductCategoryList(id=str(id), items=product_items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch('/')
async def edit_product_category(product_category_id: str,
                            product_type_to_update: UpdateProductCategory, current_user=Depends(is_seller)):
    try:
        product_type_to_update = dict(product_type_to_update)
        product_type_to_update = {k: v for k, v in product_type_to_update.items() if v is not None}
        update_product_category({'_id': ObjectId(product_category_id)}, product_type_to_update)
        return {'Message': 'Product updated'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/')
async def remove_product_category(product_category_id: str, current_user=Depends(is_seller)):
    try:
        delete_product_category({'_id': ObjectId(product_category_id)})
        return {'message': 'product category removed successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
