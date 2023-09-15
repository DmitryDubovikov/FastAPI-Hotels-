from datetime import datetime, timedelta

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    InvalidTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.dao import UserDAO


def get_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
    except JWTError:
        raise InvalidTokenFormatException
    exp: str = payload.get("exp")
    if (
        not exp
        or int(exp) < (datetime.utcnow() - timedelta(minutes=180)).timestamp()
        # у меня странный глюк, в exp после декодирования получается время ровно на 3ч меньше,
        # чем туда заложено в функции create_access_token, вычтем эти 180 минут
    ):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.fetch_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user
