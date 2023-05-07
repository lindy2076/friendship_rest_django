from uuid import UUID
from datetime import datetime

from ninja import Schema


class TokenPayload(Schema):
    user_id: UUID = None
    exp: datetime


class Message(Schema):
    detail: str


class TokenSchema(Schema):
    access_token: str
    expires: datetime
    token_type: str
