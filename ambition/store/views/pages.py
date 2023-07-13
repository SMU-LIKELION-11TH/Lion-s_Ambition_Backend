from django.http import HttpRequest, HttpResponse
from django.views.generic import View, TemplateView
from django.shortcuts import redirect

from store.models import *
from store.serializers import *


class LogoutPageView(View):
    def get(self, request:HttpRequest) -> HttpResponse :
        User.unauthenticate(request)
        return redirect('/login')


class RequireLoginTemplateView(TemplateView):
    """로그인을 필요로 하는 템플릿.

    user 에 사용자 정보를 담아서 준다.

    user.name : 사용자 이름
    user.email : 사용자 이메일
    """
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = serializeUser(User.current_user(self.request))
        return context
