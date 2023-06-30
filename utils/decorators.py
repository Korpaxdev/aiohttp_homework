from json import JSONDecodeError

from aiohttp import web
from aiohttp.web_request import Request
from sqlalchemy import select

from models.tokens_model import Tokens
from utils.database import session
from utils.messages import INCORRECT_REQUEST_BODY, NOT_AUTHORIZED, NOT_FOUND, NOT_OWNER_ADVERTISEMENT, error_message
from utils.tokens import get_token_from_headers
from utils.validation import unique_validation_field, validate_model_fields, validate_required_fields


def use_request(func):
    async def wrapper(self, **kwargs):
        request: Request = self.request
        try:
            if not request.can_read_body:
                return web.json_response(error_message(INCORRECT_REQUEST_BODY), status=400)
            json_data = await request.json()
            kwargs.update(json_data=json_data)
            return await func(self, **kwargs)
        except JSONDecodeError:
            return web.json_response(error_message(INCORRECT_REQUEST_BODY), status=400)

    return wrapper


def use_base_validation(func):
    @use_request
    async def wrapper(self, **kwargs):
        json_data = kwargs["json_data"]
        errors = validate_required_fields(json_data, self.model.required_fields)
        if errors:
            return web.json_response(error_message(errors), status=400)
        kwargs.update(dict(json_data=json_data))
        return await func(self, **kwargs)

    return wrapper


def use_validation(func):
    @use_request
    async def wrapper(self, **kwargs):
        json_data = kwargs["json_data"]
        errors = await validate_model_fields(json_data, self.model)
        if errors:
            return web.json_response(error_message(errors), status=400)
        kwargs.update(dict(json_data=json_data))
        return await func(self, **kwargs)

    return wrapper


def use_unique_validation(func):
    @use_request
    async def wrapper(self, **kwargs):
        json_data = kwargs["json_data"]
        for key in self.model.required_fields:
            if key in json_data:
                errors = await unique_validation_field(key, json_data[key], self.model)
                if errors:
                    return web.json_response(error_message(errors), status=400)
        return await func(self, **kwargs)

    return wrapper


def use_entry_by_id(func):
    async def wrapper(self, **kwargs):
        async with session() as conn:
            record_id = self.request.match_info["id"]
            res = await conn.scalars(select(self.model).where(self.model.id == record_id))
            entry = res.first()
            if not entry:
                return web.json_response(error_message(NOT_FOUND), status=404)
            kwargs.update(dict(entry=entry, conn=conn))
            return await func(self, **kwargs)

    return wrapper


def use_auth_permission(func):
    async def wrapper(self, **kwargs):
        async with session() as conn:
            token = get_token_from_headers(self.request.headers)
            if not token:
                return web.json_response(error_message(NOT_AUTHORIZED), status=401)
            res = await conn.scalars(select(Tokens).filter_by(token=token))
            entry = res.first()
            if not entry:
                return web.json_response(error_message(NOT_AUTHORIZED), status=401)
        kwargs.update(dict(user_id=entry.user_id, token=token))
        return await func(self, **kwargs)

    return wrapper


def use_owner_permission(func):
    @use_auth_permission
    @use_entry_by_id
    async def wrapper(self, **kwargs):
        entry = kwargs.get("entry")
        user_id = kwargs.get("user_id")
        owner_id = entry.owner
        if owner_id != user_id:
            return web.json_response(error_message(NOT_OWNER_ADVERTISEMENT), status=403)
        return await func(self, **kwargs)

    return wrapper
