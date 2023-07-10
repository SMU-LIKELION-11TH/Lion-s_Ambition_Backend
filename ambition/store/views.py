from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from store.models import Category
from django.contrib.auth import logout
from .serializers import serializeUser
from django.contrib import auth



# Create your views here.

class UserCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse({'message': '이메일의 형식이 옳지 않습니다. 입력하신 내용을 다시 확인해주세요.'}, status=400)  # Invalid email format

        store.objects.create(
            name=data['name'],
            email=data['email'],
            token=data['token'],
        )
        return HttpResponse({'message': '회원가입 완료'}, status=201)  # Successful user create

    def get(self, request):  # save user data
        User_data = store.objects.values()
        return HttpResponse({'users': list(User_data)}, status=200)



class UserLoginView(View):

<<<<<<< HEAD
=======
    @dataclasses.dataclass
    class RequestDTO:
        email: str
        password: str

    def post(self, request: HttpRequest) -> HttpResponse:
        """사용자/로그인"""
        try:
            dto = self.parse_request_body(request)
            # TODO: 로그인 기능 구현, redirect 어디로?
            email = dto.email
            password = dto.password
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return HttpResponse(status=HTTPStatus.BAD_REQUEST)
            user = auth.authenticate(request, email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return JsonResponse(status=HTTPStatus.OK, data={
                    "message": "로그인에 성공하였습니다.",
                    "data":{
                        "user": serializeUser(user)
                    }
                })
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
>>>>>>> 14babd3245ae6b038e7e9b76f8e853d9c2d472c0


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
