from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.login import login
from routers.user import user
from routers.seller import seller
from routers.upload import upload
from routers.productCategory import productCategory
from routers.product import product
from routers.cart import cart

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "bulkHub started"}

app.include_router(
    login.router,
    prefix="/login",
    tags=["login"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "no login"}},
)

app.include_router(
    user.router,
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "no users"}},
)

app.include_router(
    seller.router,
    prefix="/seller",
    tags=["seller"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "no seller"}},
)

app.include_router(
    upload.router,
    prefix="/upload",
    tags=["upload"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "no upload"}},
)

app.include_router(
    productCategory.router,
    prefix="/productCategory",
    tags=["productCategory"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "no product category"}},
)

app.include_router(
    product.router,
    prefix="/products",
    tags=["products"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "no products"}},
)

app.include_router(
    cart.router,
    prefix="/user/cart",
    tags=["cart"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "no cart"}},
)