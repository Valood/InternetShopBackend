from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from InternetShopBackend.API.models import Product
from InternetShopBackend.API.serializers import ProductSerializer


class ProductApiView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

