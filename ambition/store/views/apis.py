from http import HTTPStatus
from typing import *

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from store.dto import *
from store.exceptions import *
from store.models import *
from store.serializers import *

# Create your views here.


def check_user_logged_in(request):
    """만약 로그인이 되어있지 않다면 UserNotLoggedInException 을 발생시킵니다."""
    User.current_user(request)


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
    "/signup"

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
    "/login"

    def post(self, request: HttpRequest) -> HttpResponse:
        """사용자/로그인"""
        try:
            dto = UserLoginDTO.from_request(request)
            entity = User.authenticate(request, dto)
            return JsonResponse(status=HTTPStatus.MOVED_PERMANENTLY, data={
                "data": {
                    "user": serializeUser(entity),
                },
            })
        except ValueError:
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)
        except ValidationError:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)


class UserLogoutView(View):
    "/logout"

    def get(self, request: HttpRequest) -> HttpResponse:
        """사용자/로그아웃"""
        try:
            check_user_logged_in(request)
            User.unauthenticate(request)
            return HttpResponse(status=HTTPStatus.MOVED_PERMANENTLY)
        except UserNotLoggedInException:
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)


class OrderView(View):
    "/order"

    def get(self, request: HttpRequest) -> HttpResponse:
        """주문/조회/여러 항목 조회"""
        try:
            check_user_logged_in(request)
            dto = OrderQueryDTO.from_request(request)
            entities = Order.query_from_dto(dto)
            return JsonResponse(status=HTTPStatus.OK, data={
                "data": {
                    "orders": list(map(serializeOrder, entities)),
                }
            })
        except (ValueError, ObjectDoesNotExist):
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)
        except UserNotLoggedInException:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)

    def post(self, request: HttpRequest) -> HttpResponse:
        """주문/생성"""
        try:
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

    def get(self, request: HttpRequest, order_id: int) -> HttpResponse:
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

    def patch(self, request: HttpRequest, order_id: int) -> HttpResponse:
        """주문/수정"""
        try:
            check_user_logged_in(request)
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
        except UserNotLoggedInException:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)


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
        try:
            check_user_logged_in(request)
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
        except UserNotLoggedInException:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)


class ProductIdView(View):
    "/product/{id}"

    def patch(self, request: HttpRequest, product_id: int) -> HttpResponse:
        """상품/수정"""
        try:
            check_user_logged_in(request)
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
        except UserNotLoggedInException:
            return HttpResponse(status=HTTPStatus.UNAUTHORIZED)


class CategoryView(View):
    "/category"

    def get(self, request: HttpRequest) -> HttpResponse:
        """카테고리/조회"""
        categories = Category.objects.all()
        return JsonResponse(status=HTTPStatus.OK, data={
            "data": {
                "categories": list(map(serializeCategory, categories)),
            },
        })
