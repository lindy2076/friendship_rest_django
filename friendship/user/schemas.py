from uuid import UUID

from ninja import Schema


class UserSchema(Schema):
    username: str
    id: UUID


class UserRegistrationSchema(Schema):
    username: str
    password: str
