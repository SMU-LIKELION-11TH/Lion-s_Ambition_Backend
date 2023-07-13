from __future__ import annotations

import dataclasses
import json
from typing import *

from django.core.validators import validate_email
from django.http import HttpRequest


REQUEST_BODY_PARSER = json.loads


@dataclasses.dataclass
class EmailValidationRequestDTO:
    @classmethod
    def from_request(cls, request: HttpRequest) -> EmailValidationRequestDTO:
        """Request Body로부터 DTO 인스턴스를 생성합니다.

        :raises django.core.exceptions.ValidationError: 이메일 형식이 아닐 경우에 발생.
        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        """
        return cls.from_dict(REQUEST_BODY_PARSER(request.body))

    @classmethod
    def from_dict(cls, data: Dict) -> EmailValidationRequestDTO:
        """Dict로부터 DTO 인스턴스를 생성합니다.

        :raises django.core.exceptions.ValidationError: 이메일 형식이 아닐 경우에 발생.
        :raises KeyError: 키 "email"이 포함되지 않은 경우에 발생.
        """
        validate_email(data['email'])
        return EmailValidationRequestDTO(email=data['email'])

    email: str


@dataclasses.dataclass
class UserRegistrationDTO:
    @classmethod
    def from_request(cls, request: HttpRequest) -> UserRegistrationDTO:
        """Request Body로부터 DTO 인스턴스를 생성합니다.

        :raises django.core.exceptions.ValidationError: 이메일 형식이 아닐 경우에 발생.
        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        """
        return cls.from_dict(REQUEST_BODY_PARSER(request.body))

    @classmethod
    def from_dict(cls, data: Dict) -> UserRegistrationDTO:
        """Dict로부터 DTO 인스턴스를 생성합니다.

        :raises django.core.exceptions.ValidationError: 이메일 형식이 아닐 경우에 발생.
        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        """
        validate_email(data['email'])
        return UserRegistrationDTO(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            validation=data['validation-code'],
        )

    email: str
    password: str
    name: str
    validation: str


@dataclasses.dataclass
class UserLoginDTO:
    @classmethod
    def from_request(cls, request: HttpRequest) -> UserLoginDTO:
        """Request Body로부터 DTO 인스턴스를 생성합니다.

        :raises django.core.exceptions.ValidationError: 이메일 형식이 아닐 경우에 발생.
        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        """
        return cls.dict(REQUEST_BODY_PARSER(request.body))

    @classmethod
    def dict(cls, data: Dict) -> UserLoginDTO:
        """Dict로부터 DTO 인스턴스를 생성합니다.

        :raises django.core.exceptions.ValidationError: 이메일 형식이 아닐 경우에 발생.
        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        """
        validate_email(data['email'])
        return UserLoginDTO(
            email=data['email'],
            password=data['password'],
        )

    email: str
    password: str


@dataclasses.dataclass
class ProductCreationDTO:
    @classmethod
    def from_request(cls, request: HttpRequest) -> ProductCreationDTO:
        """Request Body Parameters로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 데이터가 있을 경우에 발생.
        :raises ValueError: 입력 데이터의 형식이 올바르지 않은 경우에 발생.
        """
        return cls.from_dict(REQUEST_BODY_PARSER(request.body))

    @classmethod
    def from_dict(cls, data: Dict) -> ProductCreationDTO:
        """Dict로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        :raises ValueError: items 속성의 형식이 올바르지 않은 경우에 발생.
        """
        dto = ProductCreationDTO(
            category_id=int(data['category-id']),
            name=data['name'],
            price=int(data['price']),
            image_url=data['image-url'],
            soldout=data['soldout'],
        )
        if isinstance(dto.soldout, str):
            dto.soldout = dto.soldout == 'true'
        elif isinstance(dto.soldout, bool):
            dto.soldout = dto.soldout
        return dto

    category_id: int
    name: str
    image_url: str
    price: int
    soldout: bool


@dataclasses.dataclass
class ProductQueryDTO:
    @classmethod
    def from_request(cls, request: HttpRequest) -> ProductQueryDTO:
        """Request Query Parameters로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 데이터가 있을 경우에 발생.
        :raises ValueError: 입력 데이터의 형식이 올바르지 않은 경우에 발생.
        """
        return cls.from_dict(request.GET)

    @classmethod
    def from_dict(cls, data: Dict) -> ProductQueryDTO:
        """Dict로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        :raises ValueError: items 속성의 형식이 올바르지 않은 경우에 발생.
        """
        dto = ProductQueryDTO(
            category_id=data.get('category-id', None),
            soldout=data.get('soldout', None),
        )
        if isinstance(dto.soldout, str):
            dto.soldout = dto.soldout == 'true'
        return dto

    category_id: Optional[int]
    soldout: Optional[bool]


@dataclasses.dataclass
class ProductModificationDTO:
    category_id: Optional[int]
    name: Optional[str]
    image_url: Optional[str]
    price: Optional[int]
    soldout: Optional[bool]

    @classmethod
    def from_request(cls, request: HttpRequest) -> ProductModificationDTO:
        """Request Body Parameters로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 데이터가 있을 경우에 발생.
        :raises ValueError: 입력 데이터의 형식이 올바르지 않은 경우에 발생.
        """
        return cls.from_dict(REQUEST_BODY_PARSER(request.body))

    @classmethod
    def from_dict(cls, data: Dict) -> ProductModificationDTO:
        """Dict로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        :raises ValueError: items 속성의 형식이 올바르지 않은 경우에 발생.
        """
        dto = ProductModificationDTO(
            category_id=data.get('category-id'),
            name=data.get('name'),
            price=data.get('price'),
            image_url=data.get('image-url'),
            soldout=data.get('soldout'),
        )
        if dto.category_id is not None:
            dto.category_id = int(dto.category_id)
        if dto.price is not None:
            dto.price = int(dto.price)
        if dto.soldout is not None:
            if isinstance(dto.soldout, str):
                dto.soldout = dto.soldout == 'true'
            elif isinstance(dto.soldout, bool):
                dto.soldout = dto.soldout
            else:
                raise ValueError()
        return dto


@dataclasses.dataclass
class OrderItemDTO:
    product_id: int
    quantity: int


@dataclasses.dataclass
class OrderCreationDTO:
    @classmethod
    def from_request(cls, request: HttpRequest) -> OrderCreationDTO:
        """Request Body로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 데이터가 있을 경우에 발생.
        :raises ValueError: 입력 데이터의 형식이 올바르지 않은 경우에 발생.
        """
        return cls.from_dict(REQUEST_BODY_PARSER(request.body))

    @classmethod
    def from_dict(cls, data: Dict) -> OrderCreationDTO:
        """Dict로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        :raises ValueError: items 속성의 형식이 올바르지 않은 경우에 발생.
        """
        dto = OrderCreationDTO(
            items=[],
        )
        try:
            if not isinstance(data['items'], list):
                raise ValueError()
        except json.JSONDecodeError:
            raise ValueError()
        for item in data['items']:
            item_dto = OrderItemDTO(
                product_id=int(item['product-id']),
                quantity=int(item['quantity']),
            )
            dto.items.append(item_dto)
        return dto

    items: List[OrderItemDTO]


@dataclasses.dataclass
class OrderQueryDTO:
    @classmethod
    def from_request(cls, request: HttpRequest) -> OrderQueryDTO:
        """Request Body로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 데이터가 있을 경우에 발생.
        :raises ValueError: 입력 데이터의 형식이 올바르지 않은 경우에 발생.
        """
        return cls.from_dict(request.GET)

    @classmethod
    def from_dict(cls, dict: Dict) -> OrderQueryDTO:
        """Dict로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        :raises ValueError: 속성의 형식이 올바르지 않은 경우에 발생.
        """
        dto = OrderQueryDTO(
            create_year=dict.get('year'),
            create_month=dict.get('month'),
            status=dict.get('status'),
        )
        if dto.create_year is not None:
            dto.create_year = int(dto.create_year)
        if dto.create_month is not None:
            dto.create_month = int(dto.create_month)
        if dto.status is not None:
            dto.status = int(dto.status)
        return dto

    create_year: Optional[int]
    create_month: Optional[int]
    status: Optional[int]


@dataclasses.dataclass
class OrderModificationDTO:
    @classmethod
    def from_request(cls, request: HttpRequest) -> OrderModificationDTO:
        """Request Body로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 데이터가 있을 경우에 발생.
        :raises ValueError: 입력 데이터의 형식이 올바르지 않은 경우에 발생.
        """
        return cls.from_dict(REQUEST_BODY_PARSER(request.body))

    @classmethod
    def from_dict(cls, data: Dict) -> OrderModificationDTO:
        """Dict로부터 DTO 인스턴스를 생성합니다.

        :raises KeyError: 누락된 속성이 있을 경우에 발생.
        :raises ValueError: 속성의 형식이 올바르지 않은 경우에 발생.
        """
        dto = OrderModificationDTO(
            status=int(data['status']),
        )
        return dto

    status: int
