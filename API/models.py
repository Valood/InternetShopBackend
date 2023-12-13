from django.db import models
from ..Auth.models import *

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=30, null=True)
    price = models.FloatField(null=True)
    description = models.TextField(max_length=300, null=True)
    image = models.TextField(null=True)

class Order(models.Model):
    status = models.CharField(max_length=30, default="Обрабатывается")
    date = models.DateTimeField()


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="author")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comment_product")
    message = models.TextField(max_length=300, null=True)

