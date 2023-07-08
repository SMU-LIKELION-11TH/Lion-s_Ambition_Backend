from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from store.models import Category

# Create your views here.


class UserCreateView(View):
    "/signup"
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

    def post(self, request: HttpRequest) -> HttpResponse:
        """사용자/추가(회원가입)"""
        pass
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse({'message': '이메일의 형식이 옳지 않습니다. 입력하신 내용을 다시 확인해주세요.'}, status=400)  # Invalid email format

        verification_code = generate_verification_code()  # Generate a random verification code
        send_verification_email(email, verification_code)  # Send the verification code

class UserLoginView(View):
    "/login"
        store.objects.create(
            name=data['name'],
            email=data['email'],
            token=data['token'],
            verification_code=verification_code,  # Save the verification code to the user model
        )
        return HttpResponse({'message': '회원가입 완료'}, status=201)  # Successful user create

    def post(self, request: HttpRequest) -> HttpResponse:
        """사용자/로그인"""
        pass
    def get(self, request):  # save user data
        User_data = User.objects.values()
        return JsonResponse({'users': list(User_data)}, status=200)

def generate_verification_code():
    return str(random.randint(10000, 99999))  # random 5-digit verification code

def send_verification_email(email, verification_code):
    #  .....모르겠어요...


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
