from django.http import HttpRequest, HttpResponse
from django.views.generic import View

# Create your views here.


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

    def get(self, request: HttpRequest) -> HttpResponse:
        """주문/조회/단일 항목 조회"""
        pass

    def patch(self, request: HttpRequest) -> HttpResponse:
        """주문/수정"""
        pass


class ProductView(View):
    "/product"

    def get(self, request: HttpRequest) -> HttpResponse:
        """상품/조회/여러 항목 조회"""
        pass

    def post(self, request: HttpRequest) -> HttpResponse:
        """상품/추가"""
        pass


class ProductIdView(View):
    "/product/{id}"

    def patch(self, request: HttpRequest) -> HttpResponse:
        """상품/수정"""
        pass


class CategoryView(View):
    "/category"

    def get(self, request: HttpRequest) -> HttpResponse:
        """카테고리/조회"""
        pass
