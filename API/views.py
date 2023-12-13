from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class ProductApiView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductsApiView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderApiView(APIView):
    def post(self, request):
        author = request.user
        products_index = request.data["products"]
        order = Order(user=author, date=datetime.now())
        order.save()
        for index in products_index:
            ProductOrder.objects.create(product_id=index, order=order)
        return Response("create", status=status.HTTP_200_OK)

class OrdersApiView(APIView):

    def get(self, request):
        response_lst = []
        user = request.user
        user_orders = Order.objects.filter(user=user)
        for order in user_orders:
            order_dct = {"id": order.id, "date": order.date, "orders": []}
            user_product_orders = ProductOrder.objects.filter(order=order)
            for product_order in user_product_orders:
                order_dct["products"].append(ProductSerializer(product_order.product).data)
            response_lst.append(order_dct)
        return Response(response_lst, status=status.HTTP_200_OK)

