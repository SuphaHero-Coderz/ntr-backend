import passlib.hash as _hash
import enum

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class OrderStatus(enum.Enum):
    pending = 0
    payment = 1
    delivery = 2
    complete = 3


class UserCredentials(BaseModel):
    username: str
    password: str

class OrderInformation(BaseModel):
    num_tokens: int


class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    orders: List["Order"] = Relationship(back_populates="user")

    def verify_password(self, password: str) -> bool:
        return _hash.bcrypt.verify(password, self.hashed_password)


class Order(SQLModel, table=True):
    __tablename__: str = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    user: Optional[User] = Relationship(back_populates="orders")
    num_tokens: int
    payment_id: int
    payment_status: bool
    delivery_status: bool
    status: OrderStatus
    created_at: datetime


class Payment(SQLModel):
    __tablename__: str = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    payment_amount: float
    timestamp: datetime
