from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path("product/<int:pk>", ProductApiView.as_view()),
    path("product", ProductApiView.as_view()),
]