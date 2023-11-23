import src.db_services as _services

from src.routers import users, orders
from .redis import RedisResource
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

app = FastAPI()

_services.create_database()

load_dotenv()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(orders.router)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": "Unauthorized access"})


@app.get("/")
def read_root():
    return {"Hello": "World"}
