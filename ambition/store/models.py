from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(verbose_name='이름', max_length=16)
    email = models.EmailField(verbose_name='이메일', max_length=64)
    token = models.CharField(verbose_name='비밀번호', max_length=64)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, db_column=Category.pk)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    primary_image_url = models.CharField(max_length=200, null=False)
    regular_price = models.IntegerField(null=False)
    is_soldout = models.BooleanField()
