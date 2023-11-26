import src.db_services as _services
import logging
from src.redis import RedisResource as redis
from src.redis import Queue

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from src.models import OrderInformation, User
from sqlmodel import Session
from src.database import get_session
from opentelemetry import trace

router = APIRouter(tags=["users"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tracer = trace.get_tracer("backend.tracer")


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

    Authorize.jwt_required()
    user_id: int = Authorize.get_jwt_subject()
    user: User = await _services.get_user_by_id(user_id, session)

    with tracer.start_as_current_span("order_create") as orderspan:
        survival_bag = {
            "user_id": user_id,
            "user_credits": user.credits,
            "num_tokens": order.num_tokens,
        }
        orderspan.add_event("Order created")
        orderspan.set_attribute("order.info", survival_bag)
        logger.info("Pushing order info to Order Creation service: ", survival_bag)
        redis.push_to_queue(Queue.order_queue, survival_bag)

        return {"message": "Order created"}
