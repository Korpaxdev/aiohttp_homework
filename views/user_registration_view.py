from aiohttp import web

from models.users_model import Users
from utils.database import session
from utils.decorators import use_validation
from utils.messages import error_message
from utils.validation import validate_password_field


class UserRegistration(web.View):
    model = Users

    @use_validation
    async def post(self, json_data, **kwargs):
        async with session() as conn:
            errors = validate_password_field(json_data["password"])
            if errors:
                return web.json_response(error_message(errors), status=400)
            user = self.model(**json_data)
            conn.add(user)
            await conn.commit()
            return web.json_response(user.to_dict(["id", "email"]))
