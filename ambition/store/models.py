from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=16)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    kakao_oauth_token = models.CharField(max_length=64)


class EmailValidation(models.Model):
    email = models.EmailField(max_length=64)
    codes = models.EmailField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    primary_image_url = models.CharField(max_length=200, null=False)
    regular_price = models.IntegerField(null=False)
    is_soldout = models.BooleanField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
