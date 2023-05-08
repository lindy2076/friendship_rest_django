"""
URL configuration for friendship project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.http import Http404
from ninja import NinjaAPI, errors

from user.views import user
from auth.views import auth
from friendship_service.views import friends


api = NinjaAPI()

api.title = "Friendship Service API"
api.description = "Сервис, в котором можно добавлять в друзья."

api.add_router('/users', user)
api.add_router('/auth', auth)
api.add_router('/friends', friends)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls)
]


@api.exception_handler(Http404)
def not_found_errors(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=404)


@api.exception_handler(errors.ValidationError)
def validation_errors(request, exc):
    return api.create_response(request, {"detail": str(exc.errors)}, status=422)
