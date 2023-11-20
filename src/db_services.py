import src.database as _database

from passlib.hash import bcrypt
from sqlmodel import Session, select
from src.database import engine
from src.models import User, Inventory, InventoryItem
from src.routers.users import UserCredentials

DEFAULT_TOKEN_AMOUNT = 100

"""
DATABASE ZONE
"""


def create_database() -> None:
    """
    Initializes the database engine
    """
    _database.init_db()


def populate_inventory() -> None:
    """
    Populates the inventory table with tokens
    """
    with Session(engine) as session:
        tokens = [
            Inventory(token_type=token_type.value, amount=DEFAULT_TOKEN_AMOUNT)
            for token_type in InventoryItem
        ]
        session.add_all(tokens)
        session.commit()


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
    user_obj = User(username=user.username, hashed_password=bcrypt.hash(user.password))

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
