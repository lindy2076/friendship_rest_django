from enum import Enum
from uuid import UUID
from typing import List
from ninja import Schema, ModelSchema

from user.schemas import UserSchema
from .models import Friendship


class FriendshipStatus(str, Enum):
    NONE: str = "none"
    OUTGOING: str = "outgoing"
    INCOMING: str = "incoming"
    FRIENDS: str = "friends"


class FriendshipStatusSchema(Schema):
    """
    Статусы дружбы: none/outgoing/incoming/friends
    """
    status: str 


class FriendshipRequestsSchema(Schema):
    incoming: List[UserSchema]
    outgoing: List[UserSchema]
