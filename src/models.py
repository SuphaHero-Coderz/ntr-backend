import passlib.hash as _hash

from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import BaseModel
from pydantic import Field as PyField


class UserCredentials(BaseModel):
    username: str
    password: str


class OrderInformation(BaseModel):
    num_tokens: int = PyField(gt=0)
    order_fail: bool = PyField(default=False)
    payment_fail: bool = PyField(default=False)
    inventory_fail: bool = PyField(default=False)
    delivery_fail: bool = PyField(default=False)


class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    credits: Optional[int] = Field(default=100)

    def verify_password(self, password: str) -> bool:
        return _hash.bcrypt.verify(password, self.hashed_password)
