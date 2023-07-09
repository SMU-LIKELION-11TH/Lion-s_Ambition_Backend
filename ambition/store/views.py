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
            code = self.generate_random_code(5)
            self.send_email(dto, code)
            self.save_entity(dto, code)
            return HttpResponse(status=HTTPStatus.OK)
        except (KeyError, ValueError):
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)

    def parse_request_body(self, request: HttpRequest) -> RequestDTO:
        # TODO: 이메일 주소 형식이 올바른지 검사하기.
        data = QueryDict(request.body)
        return EmailValidationView.RequestDTO(email=data['email'])

    def generate_random_code(self, length: int) -> str:
        """임시로 발급할 알파벳 n자리의 코드를 임의로 생성합니다."""
        codes = []
        for i in range(length):
            codes.append(chr(random.randint(ord('A'), ord('Z'))))
        return ''.join(codes)

    def send_email(self, dto: RequestDTO, code: str) -> EmailMessage:
        email = EmailMessage()
        email.subject = "야심작 이메일 인증번호"
        email.body = f"인증번호는 {code}입니다."
        email.to = [dto.email]
        email.send()

    def save_entity(self, dto: RequestDTO, code: str) -> EmailValidation:
        entity, is_created = EmailValidation.objects.get_or_create(email=dto.email)
        entity.codes = code
        entity.created_at = datetime.datetime.now()
        entity.save()


class UserCreateView(View):
    "/signup"

    @dataclasses.dataclass
    class RequestDTO:
        email: str
        password: str
        name: str
        validation_code: str

    def post(self, request: HttpRequest) -> HttpResponse:
        """사용자/추가(회원가입)"""
        try:
            dto = self.parse_request_body(request)
            self.check_email_validation_code(dto)
            user = self.create_user(dto)
            return JsonResponse(status=HTTPStatus.CREATED, data={
                "message": "회원가입에 성공하였습니다.",
                "data": {
                    "user": {
                        "id": user.pk,
                        "name": user.name,
                        "email": user.email,
                    }
                }
            })
        except ValueError:
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)
        except (AssertionError, ObjectDoesNotExist):
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)
        except IntegrityError:
            return HttpResponse(status=HTTPStatus.CONFLICT)

    def parse_request_body(self, request: HttpRequest) -> RequestDTO:
        data = QueryDict(request.body)
        return UserCreateView.RequestDTO(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            validation_code=data['validation-code'],
        )

    def check_email_validation_code(self, dto: RequestDTO):
        entity = EmailValidation.objects.get(email=dto.email)
        if entity.codes != dto.validation_code:
            raise AssertionError()

    def create_user(self, dto: RequestDTO) -> User:
        entity = User()
        entity.name = dto.name
        entity.email = dto.email
        entity.password = dto.password
        entity.kakao_oauth_token = None
        entity.save()
        return entity


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
