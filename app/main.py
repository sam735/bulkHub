from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.login import login

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
    responses={404: {"description": "no sellers"}},
)