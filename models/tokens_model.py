import uuid

from sqlalchemy import Column, ForeignKey, Integer, String

from models.base_model import Base


class Tokens(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        self.token = uuid.uuid4().hex
        super().__init__()
