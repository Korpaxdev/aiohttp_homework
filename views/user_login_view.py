from aiohttp import web

from models.tokens_model import Tokens
from models.users_model import Users
from utils.database import session
from utils.decorators import use_base_validation
from utils.messages import error_message
from utils.tokens import check_is_login, remove_token
from utils.users import get_user_by_json_data


class UserLogin(web.View):
    model = Users

    @use_base_validation
    async def post(self, json_data):
        async with session() as conn:
            user, error = await get_user_by_json_data(json_data)
            if error and not user:
                return web.json_response(error_message(error), status=400)
            if await check_is_login(user.id):
                await remove_token(user_id=user.id)
            token = Tokens(user_id=user.id)
            conn.add(token)
            await conn.commit()
            return web.json_response(token.to_dict(["token"]))
