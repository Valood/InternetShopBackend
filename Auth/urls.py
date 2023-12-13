from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path("registration", RegistrationAPIView.as_view()),
    path("login", LoginApiView.as_view()),
]