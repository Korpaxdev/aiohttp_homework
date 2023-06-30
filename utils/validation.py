from sqlalchemy import select

from utils.database import session
from utils.messages import PASSWORD_TOO_SHORT, REQUIRED_FIELD, TOO_LONG_FIELD, UNIQUE_FIELD


def validate_required_fields(json_data, required_fields: list | tuple) -> list:
    errors = []
    for field in required_fields:
        if field not in json_data:
            errors.append({field: REQUIRED_FIELD})
    return errors


async def unique_validation_field(field: str, data_value, model) -> list:
    errors = []
    column = model.__table__.columns[field]
    if getattr(column, "unique", False):
        async with session() as conn:
            res = await conn.scalars(select(model).filter(column == data_value))
            if res.first():
                errors.append({field: UNIQUE_FIELD})
    return errors


async def validate_model_fields(json_data, model) -> list:
    errors = []
    required_errors = validate_required_fields(json_data, model.required_fields)
    if required_errors:
        return required_errors

    for field in model.required_fields:
        column = model.__table__.columns[field]
        data_value = json_data[field]
        column_length = getattr(column.type, "length", None)
        if column_length and len(str(data_value)) > column_length:
            errors.append({field: TOO_LONG_FIELD.format(column_length)})
        unique_errors = await unique_validation_field(field, data_value, model)
        if unique_errors:
            errors.append(*unique_errors)
    return errors


def validate_password_field(password) -> list:
    errors = []
    if len(str(password)) < 8:
        errors.append({"password": PASSWORD_TOO_SHORT})
    return errors
