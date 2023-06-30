import re
import uuid

from sqlalchemy import select

from models.tokens_model import Tokens
from utils.database import session


async def check_is_login(user_id: int):
    async with session() as conn:
        res = await conn.scalars(select(Tokens).filter_by(user_id=user_id))
        token = res.first()
        return bool(token)


async def remove_token(token: str = None, user_id: int = None):
    if token is None and user_id is None:
        return False
    async with session() as conn:
        if token:
            res = await conn.scalars(select(Tokens).filter_by(token=token))
        else:
            res = await conn.scalars(select(Tokens).filter_by(user_id=user_id))
        entry = res.first()
        if not entry:
            return False
        await conn.delete(entry)
        await conn.commit()
        return True


def get_token_from_headers(headers):
    authorization = headers.get("Authorization")
    if not authorization:
        return None
    token = re.match(r"Token\s+(.+)", authorization)
    if token and token.group(1):
        return get_uuid_from_string(token.group(1))
    return None


def get_uuid_from_string(string: str):
    try:
        return uuid.UUID(string)
    except ValueError:
        return None
