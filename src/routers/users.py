import src.db_services as _services

from src.database import get_session
from sqlmodel import Session
from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from src.models import UserCredentials

# Reference: IndominusByte's JWT In Cookies

router = APIRouter(tags=["users"])


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post("/register", status_code=201)
async def register(
    user: UserCredentials,
    Authorize: AuthJWT = Depends(),
    session: Session = Depends(get_session),
):
    """
    Registers a new user

    Args:
        user (User): user information object
        Authorize (AuthJWT, optional): authorization handler. Defaults to Depends().
        session (Session, optional): database session. Defaults to Depends(get_session).

    Raises:
        HTTPException: in case username already exists

    Returns: response object
    """
    db_user = await _services.get_user_by_username(user.username, session)

    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    created_user = await _services.create_user(user, session)

    access_token = Authorize.create_access_token(subject=created_user.id)
    refresh_token = Authorize.create_refresh_token(subject=created_user.id)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return {"message": "Registration successful"}


@router.post("/login")
async def login(
    user: UserCredentials,
    Authorize: AuthJWT = Depends(),
    session: Session = Depends(get_session),
):
    """
    Logs a user in

    Args:
        user (User): user information object
        Authorize (AuthJWT, optional): authorization handler. Defaults to Depends().
        session (Session, optional): database session. Defaults to Depends(get_session).

    Raises:
        HTTPException: in case credentials invalid

    Returns: response object
    """
    credentials_valid = await _services.authenticate_user(
        username=user.username, password=user.password, session=session
    )

    if not credentials_valid:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)

    return {"message": "Login successful"}


@router.post("/refresh")
async def refresh(Authorize: AuthJWT = Depends()):
    """
    Refreshes the current JWT token

    Args:
        Authorize (AuthJWT, optional): authentication handler. Defaults to Depends().

    Returns: response object
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    Authorize.set_access_cookies(new_access_token)

    return {"message": "Token refreshed"}


@router.get("/get-user")
async def get_user(user_id: int, session: Session = Depends(get_session)):
    user = await _services.get_user_by_id(user_id, session)
    return user


@router.put("/add-credits")
async def add_credits(
    user_id: int,
    num_credits: int,
    Authorize: AuthJWT = Depends(),
    session: Session = Depends(get_session),
):
    """
    Adds credits to the user's balance

    Args:
        user_id (int): id to add
        num_credits (int): credits to add
        Authorize (AuthJWT, optional): authentication handler. Defaults to Depends().

    Returns: response object
    """
    await _services.add_credits(
        user_id=user_id, num_credits=num_credits, session=session
    )

    return {"message": "Added credits"}


@router.put("/deduct-credits")
async def deduct_credits(
    user_id: int,
    num_credits: int,
    Authorize: AuthJWT = Depends(),
    session: Session = Depends(get_session),
):
    """
    Deducts credits from the user's balance

    Args:
        user_id (int): id to add
        num_credits (int): credits to add
        Authorize (AuthJWT, optional): authentication handler. Defaults to Depends().

    Returns: response object
    """
    await _services.deduct_credits(
        user_id=user_id, num_credits=num_credits, session=session
    )

    return {"message": "Deducted credits"}


@router.delete("/logout")
async def logout(Authorize: AuthJWT = Depends()):
    """
    Logs a user out

    Args:
        Authorize (AuthJWT, optional): authorization handler. Defaults to Depends().

    Returns: response object
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()

    return {"message": "Logout successful"}
