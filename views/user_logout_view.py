from aiohttp import web

from utils.messages import LOGOUT_SUCCESS, NOT_AUTHORIZED, TOKEN_NOT_FOUND, error_message
from utils.tokens import get_token_from_headers, remove_token


class UserLogout(web.View):
    async def post(self):
        token = get_token_from_headers(self.request.headers)
        if not token:
            return web.json_response(error_message(NOT_AUTHORIZED), status=401)
        if await remove_token(token=token):
            return web.json_response(error_message(LOGOUT_SUCCESS))
        return web.json_response(error_message(TOKEN_NOT_FOUND), status=400)
