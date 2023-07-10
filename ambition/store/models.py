from __future__ import annotations

import datetime
import random

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import EmailMessage
from django.db import models

from store.dto import *

# Create your models here.


class EmailValidation(models.Model):
    @classmethod
    def create_or_update_from_dto(cls, dto: EmailValidationRequestDTO) -> EmailValidation:
        entity = cls.objects.get_or_create(email=dto.email)[0]
        entity.codes = cls.generate_codes()
        entity.created_at = datetime.datetime.now()
        entity.save()
        return entity

    @classmethod
    def validate_from_dto(cls, dto: UserRegistrationDTO) -> bool:
        try:
            entity = cls.objects.get(email=dto.email)
            if entity.codes != dto.validation:
                raise AssertionError()
            entity.delete()
            return True
        except AssertionError:
            pass
        except ObjectDoesNotExist:
            pass
        finally:
            return False

    @classmethod
    def generate_codes(cls, length=5) -> str:
        """알파벳 n자리의 인증 코드를 임의로 생성합니다."""
        codes = []
        for i in range(length):
            codes.append(chr(random.randint(ord('A'), ord('Z'))))
        return ''.join(codes)

    email = models.EmailField(primary_key=True, max_length=64)
    codes = models.EmailField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def send_email(self):
        email = EmailMessage()
        email.subject = "야심작 이메일 인증번호"
        email.body = f"인증번호는 {self.codes}입니다."
        email.to = [self.email]
        email.send()


class User(models.Model):
    @classmethod
    def create_from_dto(cls, dto: UserRegistrationDTO) -> User:
        entity = User()
        entity.name = dto.name
        entity.email = dto.email
        entity.password = dto.password
        entity.kakao_oauth_token = None
        entity.save()
        return entity

    name = models.CharField(max_length=16)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=64)
    kakao_oauth_token = models.CharField(max_length=64, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    @classmethod
    def create_from_dto(cls, dto: ProductCreationDTO) -> Product:
        entity = Product()
        entity.category = Category.objects.get(pk=int(dto.category_id))
        entity.name = dto.name
        entity.primary_image_url = dto.image_url
        entity.regular_price = dto.price
        entity.is_soldout = dto.soldout
        entity.save()
        return entity

    @classmethod
    def query_from_dto(cls, dto: ProductQueryDTO) -> models.query.QuerySet[Product]:
        kwargs = {}
        if dto.category_id is not None:
            kwargs['category'] = Category.objects.get(pk=dto.category_id)
        if dto.soldout is not None:
            kwargs['is_soldout'] = dto.soldout
        return cls.objects.filter(**kwargs)

    @classmethod
    def update_from_dto(cls, pk: int, dto: ProductModificationDTO) -> Product:
        entity = Product.objects.get(pk=pk)
        if dto.category_id is not None:
            entity.category = Category.objects.get(pk=int(dto.category_id))
        if dto.name is not None:
            entity.name = dto.name
        if dto.image_url is not None:
            entity.primary_image_url = dto.image_url
        if dto.price is not None:
            entity.regular_price = dto.price
        if dto.soldout is not None:
            entity.is_soldout = dto.soldout
        entity.save()
        return entity

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True,
                            blank=False, null=False)
    primary_image_url = models.CharField(max_length=200, null=False)
    regular_price = models.IntegerField(null=False)
    is_soldout = models.BooleanField()


class OrderStatus(models.Model):
    name = models.CharField(max_length=16)


class Order(models.Model):
    @classmethod
    def create_from_dto(cls, dto: OrderCreationDTO) -> Order:
        entities = []
        order = Order()
        order.status = OrderStatus.objects.get(pk=1)
        entities.append(order)
        for item in dto.items:
            order_item = OrderItem()
            order_item.order = order
            order_item.product = Product.objects.get(pk=item.product_id)
            order_item.unit_price = order_item.product.regular_price
            order_item.quantity = item.quantity
            entities.append(order_item)
        for entity in entities:
            entity.save()
        return order

    @classmethod
    def query_from_dto(cls, dto: OrderQueryDTO) -> models.query.QuerySet[Order]:
        kwargs = {}
        if dto.status is not None:
            kwargs['status'] = OrderStatus.objects.get(pk=dto.status)
        if dto.create_year is not None:
            kwargs['created_at__year'] = dto.create_year
        if dto.create_month is not None:
            # TODO: 월별 조회 기능 구현
            raise NotImplementedError('월별 조회 기능은 아직 지원되지 않습니다.')
        return cls.objects.filter(**kwargs)

    @classmethod
    def update_from_dto(cls, pk: int, dto: OrderModificationDTO) -> Order:
        entity = cls.objects.get(pk=pk)
        entity.status = OrderStatus.objects.get(pk=dto.status)
        entity.updated_at = datetime.datetime.now()
        entity.save()
        return entity

    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
