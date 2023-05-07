from uuid import UUID
from ninja import Schema, ModelSchema

from user.schemas import UserSchema
from .models import Friendship


class FriendshipSchema(ModelSchema):
    class Config:
        model = Friendship
        model_exclude = ["id"]

    user_from: UserSchema
    user_to: UserSchema
