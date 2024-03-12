#branch/add-branch

from django.urls import path
from .views import add_branch

urlpatterns = [
    path('add-branch', add_branch),
]