from django.urls import path
from .views import get_all_users,user_login_view,create_user

urlpatterns = [
    path('get-all/', get_all_users),
    path('login', user_login_view),
    path('create-user', create_user),
]