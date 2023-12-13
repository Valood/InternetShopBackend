from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path("product", ProductApiView.as_view()),
]