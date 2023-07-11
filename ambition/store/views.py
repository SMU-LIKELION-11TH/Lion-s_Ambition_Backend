from __future__ import annotations

import dataclasses
from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from django.views.generic import View

from store.dto import *
from store.models import *
from store.serializers import *

# Create your views here.


class EmailValidationView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        """이메일 인증 기능을 수행합니다.

        반드시 인증할 이메일 주소를 요청 Body에 포함해야합니다.
        이메일 주소가 포함 되어있지 않다면 400 BadRequest 응답코드를 반환합니다.
        """
        try:
            dto = EmailValidationRequestDTO.from_request(request)
            entity = EmailValidation.create_or_update_from_dto(dto)
            entity.send_email()
            return HttpResponse(status=HTTPStatus.OK)
        except (KeyError, ValueError):
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)


class UserCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

    def post(self, request: HttpRequest) -> HttpResponse:
        """사용자/추가(회원가입)"""
        try:
            dto = UserRegistrationDTO.from_request(request)
            is_valid = EmailValidation.validate_from_dto(dto)
            if not is_valid:
                raise ValidationError('이메일 인증 코드가 올바르지 않습니다.')
            user = User.create_from_dto(dto)
            return JsonResponse(status=HTTPStatus.CREATED, data={
                "message": "회원가입에 성공하였습니다.",
                "data": { "user": serializeUser(user) },
            })
        except ValueError:
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)
        except (AssertionError, ObjectDoesNotExist, ValidationError):
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)
        except IntegrityError:
            return HttpResponse(status=HTTPStatus.CONFLICT)


class UserLoginView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request,'login_view.html',)

    @dataclasses.dataclass
    class RequestDTO:
        email: str
        password: str

    def post(self, request: HttpRequest) -> HttpResponse:
        """사용자/로그인"""
        try:
            # TODO: 로그인 기능 구현
            dto = self.parse_request_body(request)
            email = dto.email
            password = dto.password
            for user in User.objects.all():
                if(user.email==email):
                    if(user.password==password):
                        request.session['logged_in'] = True
                        return JsonResponse(status=HTTPStatus.OK, data={
                            "message": "로그인에 성공하였습니다.",
                            "data": {
                            "user": serializeUser(user)
                        }
                    })
                    else:
                        pass
                else:
                    pass
            return render(request,'login_view.html',)
        except ValueError:
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)
        except (AssertionError, ObjectDoesNotExist):
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

    def parse_request_body(self, request: HttpRequest) -> RequestDTO:
        data = QueryDict(request.body)
        return UserLoginView.RequestDTO(
            email=data['email'],
            password=data['password'],
        )

def is_user_logged_in(request):
    return request.session.get('logged_in', False)

class UserLogoutView(View):
    "/logout"
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse({'message': '로그아웃이 성공적으로 처리되었습니다.'}, status=200)
        else:
            return HttpResponse({'message': '로그인되어 있지 않습니다.'}, status=401)

class OrderView(View):
    "/order"

    def get(self, request: HttpRequest) -> HttpResponse:
        """주문/조회/여러 항목 조회"""
        try:
            # TODO: 로그인 기능 구현
            dto = OrderQueryDTO.from_request(request)
            entities = Order.query_from_dto(dto)
            return JsonResponse(status=HTTPStatus.OK, data={
                "data": {
                    "orders": list(map(serializeOrder, entities)),
                }
            })
        except (ValueError, ObjectDoesNotExist):
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)

    def post(self, request: HttpRequest) -> HttpResponse:
        """주문/생성"""
        try:
            # TODO: 로그인 기능 구현
            dto = OrderCreationDTO.from_request(request)
            entity = Order.create_from_dto(dto)
            return JsonResponse(status=HTTPStatus.CREATED, data={
                "data": {
                    "order": serializeOrder(entity),
                }
            })
        except (KeyError, ValueError):
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)


class OrderIdView(View):
    "/order/{id}"

    def get(self, request: HttpRequest) -> HttpResponse:
        """주문/조회/단일 항목 조회"""
        try:
            entity = Order.objects.get(pk=order_id)
            return JsonResponse(status=HTTPStatus.OK, data={
                "data": {
                    "order": serializeOrder(entity)
                }
            })
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.NOT_FOUND)

    def patch(self, request: HttpRequest) -> HttpResponse:
        """주문/수정"""
        try:
            # TODO: 로그인 기능 구현
            dto = OrderModificationDTO.from_request(request)
            entity = Order.update_from_dto(order_id, dto)
            return JsonResponse(status=HTTPStatus.OK, data={
                "data": {
                    "order": serializeOrder(entity)
                }
            })
        except (KeyError, ValueError):
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.NOT_FOUND)


class ProductView(View):
    "/product"

    def get(self, request: HttpRequest) -> HttpResponse:
        """상품/조회/여러 항목 조회"""
        # TODO: pagination 기능 추가
        try:
            dto = ProductQueryDTO.from_request(request)
            entities = Product.query_from_dto(dto)
            return JsonResponse(status=HTTPStatus.OK, data={
                "data": {
                    "products": list(map(serializeProduct, entities)),
                },
            })
        except ObjectDoesNotExist:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data={"message": "Category not found"})
        except (KeyError, ValueError):
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data={})

    def post(self, request: HttpRequest) -> HttpResponse:
        """상품/추가"""
        # TODO: 사용자 인증 기능 추가
        try:
            dto = ProductCreationDTO.from_request(request)
            entity = Product.create_from_dto(dto)
            return JsonResponse(status=HTTPStatus.CREATED, data={
                "data": {
                    "product": serializeProduct(entity),
                },
            })
        except ObjectDoesNotExist:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data={"message": "Category not found"})
        except (KeyError, ValueError):
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data={})
        except IntegrityError:
            return JsonResponse(status=HTTPStatus.CONFLICT, data={})


class ProductIdView(View):
    "/product/{id}"

    def patch(self, request: HttpRequest) -> HttpResponse:
        """상품/수정"""
        # TODO: 사용자 인증 기능 추가
        try:
            dto = ProductModificationDTO.from_request(request)
            entity = Product.update_from_dto(product_id, dto)
            return JsonResponse(status=HTTPStatus.OK, data={
                "data": {
                    "product": serializeProduct(entity),
                },
            })
        except ObjectDoesNotExist:
            return JsonResponse(status=HTTPStatus.NOT_FOUND, data={})
        except (KeyError, ValueError):
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
