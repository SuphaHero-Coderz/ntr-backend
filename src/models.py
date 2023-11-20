import  passlib.hash as _hash
import enum

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime 

class OrderStatus(enum.Enum):
    ordering = 0
    payment = 1
    delivery = 2
    complete = 3

class InventoryItem(enum.Enum):
    default_token = 0

class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    orders: List["Order"] = Relationship(back_populates="orders")

    def verify_password(self, password: str) -> bool:
        return _hash.bcrypt.verify(password, self.hashed_password)

class Order(SQLModel, table=True):
    __tablename__: str = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    num_tokens: int
    payment_id: int
    payment_status: bool
    delivery_status: bool
    status: OrderStatus

class Payment(SQLModel, table=True):
    __tablename__: str = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id = Field(default=None, foreign_key="users.id")
    payment_amount: float
    timestamp: datetime

class Inventory(SQLModel, table=True):
    __tablename__: str = "inventory"
    token_type: InventoryItem 
    amount: int