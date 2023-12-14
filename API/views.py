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
        product_ratings = ProductRating.objects.filter(product=product).values_list('rating', flat=True)
        rating_lst = list(map(lambda x: x.rate, product_ratings))

        return_data = dict(serializer.data)
        if len(rating_lst) != 0:
            return_data["rating"] = sum(rating_lst)/len(rating_lst)
        else:
            return_data["rating"] = 0
        return Response(return_data, status=status.HTTP_200_OK)

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
        ProductCart.objects.filter(user=author).delete()
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
                order_dct["orders"].append(ProductSerializer(product_order.product).data)
            response_lst.append(order_dct)
        return Response(response_lst, status=status.HTTP_200_OK)


class CartApiView(APIView):
    def get(self, request):
        response_lst = []
        user = request.user
        products_in_cart = ProductCart.objects.filter(user=user)
        for productCart_object in products_in_cart:
            response_lst.append(ProductSerializer(productCart_object.product).data)
        return Response(response_lst, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        product = Product.objects.get(id=data["product"])
        ProductCart.objects.create(user=request.user, product=product)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


class CommentApiView(APIView):
    def get(self, request, pk):
        response_lst = []
        product = Product.objects.get(id=pk)
        comments = Comment.objects.filter(product=product)
        for comment in comments:
            data_dct = dict(CommentSerializer(comment).data)
            data_dct["name"] = comment.author.name
            response_lst.append(data_dct)
        return Response(response_lst, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        rating = Rating(author=request.user, rate=data["rating"])
        rating.save()
        ProductRating.objects.create(product_id=data["product"], rating=rating)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)