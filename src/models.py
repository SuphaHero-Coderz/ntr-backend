import passlib.hash as _hash
import enum

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


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
    credits: Optional[int] = Field(default=100)

    def verify_password(self, password: str) -> bool:
        return _hash.bcrypt.verify(password, self.hashed_password)
