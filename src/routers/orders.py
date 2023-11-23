import src.db_services as _services
from src.redis import RedisResource as redis
from src.redis import Queue

from src.database import get_session
from sqlmodel import Session
from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from src.models import UserCredentials, OrderInformation

# Reference: IndominusByte's JWT In Cookies

router = APIRouter(tags=["users"])

@router.post("/create-order")
async def create_order(order: OrderInformation, Authorize: AuthJWT = Depends(), session: Session = Depends(get_session)):
    Authorize.jwt_required()

    survival_bag = {
        "user_id" : Authorize.get_jwt_subject(),
        "num_tokens" : order.num_tokens
    }

    redis.push_to_queue(Queue.order_queue, survival_bag)

    return { "message" : "Order created" }