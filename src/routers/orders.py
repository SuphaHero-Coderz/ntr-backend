import requests
import json
import src.db_services as _services

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from src.models import OrderInformation, User
from sqlmodel import Session
from src.database import get_session

router = APIRouter(tags=["users"])


@router.post("/create-order", status_code=201)
async def create_order(
    order: OrderInformation,
    Authorize: AuthJWT = Depends(),
    session: Session = Depends(get_session),
):
    if order.num_tokens <= 0:
        raise HTTPException(
            status_code=422, detail="Number of tokens must be at least one."
        )

    user_id: int = Authorize.get_jwt_subject() 
    user: User = await _services.get_user_by_id(user_id, session)

    data = {
        "task": "do_work",
        "user_id": user.id,
        "num_tokens": order.num_tokens,
        "user_credits": user.credits,
    }

    requests.post("http://order-handler/create-order", json=data)

    return {"message": "Order created"}


@router.get("/get-orders", status_code=200)
async def get_orders_for_user(user_id: int):
    response = requests.get(
        "http://order-handler/get-orders", params={"user_id": user_id}
    )
    orders = json.loads(response.content)
    return orders

@router.get("/get-all-orders", status_code=200)
async def get_all_orders():
    response = requests.get(
        "http://order-handler/get-all-orders"
    )
    orders = json.loads(response.content)
    return orders
