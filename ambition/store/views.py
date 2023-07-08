from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from store.models import Category
from django.contrib.auth import logout



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
    def post(self, request):
        data = json.loads(request.body)

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse({'message': '이메일의 형식이 옳지 않습니다. 입력하신 내용을 다시 확인해주세요.'},
                                status=400)  # Invalid email format

        try:
            if store.objects.filter(email=data['email']).exists():
                user = store.objects.get(email=data['email'])

                if user.token == data['token']:
                    return HttpResponse({'message': '회원가입에 성공하였습니다.'}, status=301)  # login success
                return HttpResponse({'message': '잘못된 비밀번호입니다.'}, status=401)  # wrong password
            return HttpResponse({'message': '존재하지 않는 계정입니다.'}, status=401)  # non email
        return HttpResponse({'message': 로그인 과정에서 오류가 발생했습니다.}, status=400)



class UserLogoutView(View):
    "/logout"
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message': '로그아웃이 성공적으로 처리되었습니다.'}, status=200)
        else:
            return JsonResponse({'message': '로그인되어 있지 않습니다.'}, status=401)

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
