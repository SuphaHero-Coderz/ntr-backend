import src.database as _database
import random
import string

from passlib.hash import bcrypt
from sqlmodel import Session, select
from src.models import User
from src.routers.users import UserCredentials


"""
DATABASE ZONE
"""


def create_database() -> None:
    """
    Initializes the database engine
    """
    _database.init_db()


"""
USER ZONE
"""


async def create_user(user: UserCredentials, session: Session) -> User:
    """
    Creates a user in the database

    Args:
        user (User): user object
        session (Session): database session

    Returns:
        User: created user
    """
    user_obj = User(
        username=user.username, hashed_password=bcrypt.hash(user.password), orders=[]
    )

    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)

    return user_obj


async def create_throwaway_user(session: Session) -> User:
    """
    Creates a throwaway user in case no credentials when creating order

    Args:
        session (Session): database session

    Returns:
        User: user object
    """

    def generate_random_string(length: int = 7) -> string:
        return "".join(random.choices(string.ascii_uppercase, k=length))

    user_obj = User(
        username=generate_random_string(),
        hashed_password=bcrypt.hash(generate_random_string()),
        orders=[],
    )

    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)

    return user_obj


async def get_user_by_username(username: str, session: Session) -> User:
    """
    Fetches a user from the database by username

    Args:
        username (str): username to query
        session (Session): database session

    Returns:
        User: user object
    """
    query = select(User).where(User.username == username)
    result = session.exec(query).first()

    return result


async def get_user_by_id(id: int, session: Session) -> User:
    """
    Fetches a user from the database by id

    Args:
        id (int): id to query
        session (Session): database session

    Returns:
        User: user object
    """
    if id is None:
        throwaway_user = await create_throwaway_user(session)
        return throwaway_user

    query = select(User).where(User.id == id)
    result = session.exec(query).first()

    return result


async def authenticate_user(user: UserCredentials, session: Session) -> bool:
    """
    Checks to see if a user's credentials are valid

    Args:
        user (UserCredentials): user's credentials
        session (Session): database session

    Returns:
        bool: whether or not user's credentials valid
    """
    user = await get_user_by_username(user.username, session)

    return user and user.verify_password(user.password)
