from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(verbose_name='이름', max_length=16)
    email = models.EmailField(verbose_name='이메일', max_length=64)
    token = models.CharField(verbose_name='비밀번호', max_length=64)
