from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
