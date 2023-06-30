from aiohttp import web
from sqlalchemy import select

from models.advertisements_model import Advertisements
from utils.database import session
from utils.decorators import use_auth_permission, use_validation


class Index(web.View):
    model = Advertisements

    async def get(self, **kwargs):
        async with session() as conn:
            res = await conn.scalars(select(self.model))
            advertisements = [r.to_dict(["id", "title"]) for r in res.all()]
            return web.json_response(advertisements)

    @use_auth_permission
    @use_validation
    async def post(self, json_data, user_id, **kwargs):
        json_data["owner"] = user_id
        async with session() as conn:
            advertisement = self.model(**json_data)
            conn.add(advertisement)
            await conn.commit()
            return web.json_response(advertisement.to_dict(), status=201)
