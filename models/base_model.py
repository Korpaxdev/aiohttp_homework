from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    required_fields = []

    def to_dict(self, fields: list | tuple = None):
        if fields:
            return {k: str(getattr(self, k)) for k in fields}
        keys = self.__table__.columns.keys()
        return {k: str(getattr(self, k)) for k in keys}
