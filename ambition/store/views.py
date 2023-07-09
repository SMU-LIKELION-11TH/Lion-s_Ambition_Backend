import dataclasses
import datetime
import random
from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse, QueryDict
from django.views.generic import View

from store.models import *

# Create your views here.


class EmailValidationView(View):
    @dataclasses.dataclass
    class RequestDTO:
        email: str

    def post(self, request: HttpRequest) -> HttpResponse:
        """이메일 인증 기능을 수행합니다.

        반드시 인증할 이메일 주소를 요청 Body에 포함해야합니다.
        이메일 주소가 포함 되어있지 않다면 400 BadRequest 응답코드를 반환합니다.
        """
        try:
            dto = self.parse_request_body(request)
            codes = self.generate_random_code(5)
            self.render_email(dto.email, codes).send()
            entity, is_created = EmailValidation.objects.get_or_create(email=dto.email)
            entity.codes = codes
            entity.created_at = datetime.datetime.now()
            entity.save()
            return HttpResponse(status=HTTPStatus.OK)
        except (KeyError, ValueError):
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)

    def parse_request_body(self, request: HttpRequest) -> RequestDTO:
        """입력 형식으로부터 데이터를 추출합니다.

        입력 형식이 올바르지 않다면 ValueError를 발생시킵니다.
        """
        # TODO: 이메일 주소 형식이 올바른지 검사하기.
        data = QueryDict(request.body)
        return EmailValidationView.RequestDTO(email=data['email'])

    def generate_random_code(self, length: int) -> str:
        """임시로 발급할 알파벳 n자리의 코드를 임의로 생성합니다."""
        codes = []
        for i in range(length):
            codes.append(chr(random.randint(ord('A'), ord('Z'))))
        return ''.join(codes)

    def render_email(self, to: str, code: str) -> EmailMessage:
        email = EmailMessage()
        email.subject = "야심작 이메일 인증번호"
        email.body = f"인증번호는 {code}입니다."
        email.to = [to]
        return email


class UserCreateView(View):
    "/signup"

    def post(self, request: HttpRequest) -> HttpResponse:
        """사용자/추가(회원가입)"""
        pass


class UserLoginView(View):
    "/login"

    def post(self, request: HttpRequest) -> HttpResponse:
        """사용자/로그인"""
        pass


class UserLogoutView(View):
    "/logout"

    def get(self, request: HttpRequest) -> HttpResponse:
        """사용자/로그아웃"""
        pass


class OrderView(View):
    "/order"

    def get(self, request: HttpRequest) -> HttpResponse:
        """주문/조회/여러 항목 조회"""
        pass

    def post(self, request: HttpRequest) -> HttpResponse:
        """주문/생성"""
        pass


class OrderIdView(View):
    "/order/{id}"

    def get(self, request: HttpRequest, order_id: int) -> HttpResponse:
        """주문/조회/단일 항목 조회"""
        pass

    def patch(self, request: HttpRequest, order_id: int) -> HttpResponse:
        """주문/수정"""
        pass


class ProductView(View):
    "/product"

    def get(self, request: HttpRequest) -> HttpResponse:
        """상품/조회/여러 항목 조회"""
        try:
            data = request.GET
            query_kwargs = {}
            if 'category_id' in data:
                query_kwargs['category'] = Category.objects.get(pk=int(data.get('category_id')))
            if 'soldout' in data:
                if isinstance(data.get('soldout'), str):
                    query_kwargs['is_soldout'] = data.get('soldout') == 'true'
                elif isinstance(data.get('soldout'), bool):
                    query_kwargs['is_soldout'] = data.get('soldout')
                else:
                    raise ValueError()
            # TODO: pagination 기능 추가
            response_body = {
                "data": {
                    "products": [],
                },
            }
            for entity in Product.objects.filter(**query_kwargs):
                response_body['data']['products'].append(
                    {
                        "id": entity.pk,
                        "category": {
                            "id": entity.category.pk,
                            "name": entity.category.name,
                        },
                        "name": entity.name,
                        "image_url": entity.primary_image_url,
                        "price": entity.regular_price,
                        "is_soldout": entity.is_soldout,
                    }
                )
            return JsonResponse(status=HTTPStatus.OK, data=response_body)
        except ObjectDoesNotExist:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data={"message": "Category not found"})
        except ValueError:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data={})

    def post(self, request: HttpRequest) -> HttpResponse:
        """상품/추가"""
        # TODO: 사용자 인증 기능 추가
        try:
            data = request.POST
            product = Product()
            product.category = Category.objects.get(pk=int(data.get('category_id')))
            product.name = data.get('name')
            product.primary_image_url = data.get('image_url')
            product.regular_price = int(data.get('price'))
            if isinstance(data.get('soldout'), str):
                product.is_soldout = data.get('soldout') == 'true'
            elif isinstance(data.get('soldout'), bool):
                product.is_soldout = data.get('soldout')
            else:
                raise ValueError()
            product.save()
            return JsonResponse(status=HTTPStatus.CREATED, data={
                "data": {
                    "product": {
                        "id": product.pk,
                        "category_id": product.category.pk,
                        "category_name": product.category.name,
                        "name": product.name,
                        "image_url": product.primary_image_url,
                        "price": product.regular_price,
                        "is_soldout": product.is_soldout,
                    }
                }
            })
        except ObjectDoesNotExist:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data={"message": "Category not found"})
        except ValueError:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data={})
        except IntegrityError:
            return JsonResponse(status=HTTPStatus.CONFLICT, data={})


class ProductIdView(View):
    "/product/{id}"

    def patch(self, request: HttpRequest, product_id: int) -> HttpResponse:
        """상품/수정"""
        # TODO: 사용자 인증 기능 추가
        try:
            data = QueryDict(request.body)
            if not data:
                raise ValueError()
            product = Product.objects.get(pk=product_id)
            if 'category_id' in data:
                product.category = Category.objects.get(pk=int(data.get('category_id')))
            if 'name' in data:
                product.name = data.get('name')
            if 'image_url' in data:
                product.primary_image_url = data.get('image_url')
            if 'price' in data:
                product.regular_price = int(data.get('price'))
            if 'soldout' in data:
                if isinstance(data.get('soldout'), str):
                    product.is_soldout = data.get('soldout') == 'true'
                elif isinstance(data.get('soldout'), bool):
                    product.is_soldout = data.get('soldout')
                else:
                    raise ValueError()
            product.save()
            return JsonResponse(status=HTTPStatus.OK, data={
                "data": {
                    "product": {
                        "id": product.pk,
                        "category_id": product.category.pk,
                        "category_name": product.category.name,
                        "name": product.name,
                        "image_url": product.primary_image_url,
                        "price": product.regular_price,
                        "is_soldout": product.is_soldout,
                    }
                }
            })
        except ObjectDoesNotExist:
            return JsonResponse(status=HTTPStatus.NOT_FOUND, data={})
        except ValueError:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data={})
        except IntegrityError:
            return JsonResponse(status=HTTPStatus.CONFLICT, data={})


class CategoryView(View):
    "/category"

    def get(self, request: HttpRequest) -> HttpResponse:
        """카테고리/조회"""
        response_body = {
            "data": {
                "categories": [],
            },
        }
        for entity in Category.objects.all():
            response_body['data']['categories'].append(
                {
                    "id": entity.pk,
                    "name": entity.name
                }
            )
        return JsonResponse(data=response_body, status=HTTPStatus.OK)
