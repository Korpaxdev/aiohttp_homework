from sqlalchemy import Column, Integer, String

from models.base_model import Base
from utils.password_hash import hash_psw


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), unique=True)
    password = Column(String(128))

    required_fields = ["email", "password"]

    def __init__(self, **kwargs):
        password = kwargs["password"]
        kwargs["password"] = hash_psw(password)
        super().__init__(**kwargs)
