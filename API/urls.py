from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path("product/<int:pk>", ProductApiView.as_view()),
    path("product", ProductApiView.as_view()),

    path("products", ProductsApiView.as_view()),

    path("order/<int:pk>", OrderApiView.as_view()),
    path("order", OrderApiView.as_view()),
    path("orders", OrdersApiView.as_view()),

]