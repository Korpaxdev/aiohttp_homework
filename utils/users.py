from typing import Tuple, Type

from sqlalchemy import select

from models.users_model import Users
from utils.database import session
from utils.messages import USER_NOT_FOUND, WRONG_EMAIL_OR_PASS
from utils.password_hash import check_password

GetUserType = Tuple[Type[Users] | None, dict | None]


async def get_user_by_json_data(json_data: dict) -> GetUserType:
    async with session() as conn:
        email = json_data["email"]
        res = await conn.scalars(select(Users).filter_by(email=email))
        user = res.first()
        if not user:
            return user, USER_NOT_FOUND
        password = json_data["password"]
        if not check_password(password, user.password):
            user = None
            return user, WRONG_EMAIL_OR_PASS
        return user, None
