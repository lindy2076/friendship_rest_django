from typing import List, Optional
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import Router

from auth.jwt import AuthBearer
from auth.schemas import Message

from user.models import User
from user.schemas import UserSchema, UserRegistrationSchema
from .models import Friendship
from .schemas import FriendshipSchema

friends = Router(tags=["friends"])


@friends.get('/everything', response=List[FriendshipSchema])
def get_everything_from_db(request):
    """
    Получить все записи из бд
    """
    return Friendship.objects.all()


@friends.get('/myfriends', auth=AuthBearer(), response=List[UserSchema])
def get_my_friends(request):
    """
    Получить список своих друзей
    """
    user = request.auth
    return [user]


@friends.get('/requests', auth=AuthBearer(),
             summary="Get Incoming And Outgoing Requests")
def get_requests(request):
    ...


@friends.get('/{user_id}/all', response=List[UserSchema], 
             summary="Get User's Friends By His Id")
def get_user_friends_by_id(request, user_id):
    ...


@friends.get('/{user_id}/status', auth=AuthBearer(),
             summary="Get Friendship Status With Another User By His Id")
def get_friendship_status_by_id(request, user_id):
    ...


@friends.post('/{user_id}/add', auth=AuthBearer())
def add_friend_by_id(request, user_id):
    ...


@friends.post('/{user_id}/remove', auth=AuthBearer())
def remove_friend_by_id(request, user_id):
    ...
