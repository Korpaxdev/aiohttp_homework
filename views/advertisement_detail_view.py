from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession

from models.advertisements_model import Advertisements
from utils.decorators import use_entry_by_id, use_owner_permission, use_unique_validation, use_validation
from utils.messages import MESSAGE_DELETED, success_message


class AdvertisementDetail(web.View):
    model = Advertisements

    @use_entry_by_id
    async def get(self, entry, **kwargs):
        return web.json_response(entry.to_dict())

    @use_owner_permission
    async def delete(self, entry, conn, **kwargs):
        await conn.delete(entry)
        await conn.commit()
        return web.json_response(success_message(MESSAGE_DELETED))

    @use_owner_permission
    @use_validation
    async def put(self, json_data, entry, conn, **kwargs):
        keys = self.model.required_fields
        for key in keys:
            if key in json_data:
                setattr(entry, key, json_data[key])
        await conn.commit()
        return web.json_response(entry.to_dict())

    @use_owner_permission
    @use_unique_validation
    async def patch(self, entry, conn: AsyncSession, **kwargs):
        json_data = await self.request.json()
        available_keys = self.model.required_fields
        for key in available_keys:
            if key in json_data:
                setattr(entry, key, json_data[key])
        await conn.commit()
        return web.json_response(entry.to_dict())
