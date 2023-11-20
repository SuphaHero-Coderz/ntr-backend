import src.database as _database

from sqlmodel import Session
from src.database import engine
from src.models import Inventory, InventoryItem

DEFAULT_TOKEN_AMOUNT = 100


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
