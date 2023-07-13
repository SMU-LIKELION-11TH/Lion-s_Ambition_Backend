from django.http import HttpRequest, HttpResponse
from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect

from store.models import *

from store.serializers import *


class MainView(TemplateView):
    template_name='manage_view.html'

    def get(self, request:HttpRequest) -> HttpResponse:
        """사용자 이름 출력"""
        print(User.current_user(request))
        return render(
            request, 
            template_name= MainView.template_name, 
            context={
            'user': serializeUser(User.current_user(request))
            }
        )
    
class OrderView(TemplateView):
    template_name='ordermenu.html'

    def get(self, request:HttpRequest) -> HttpResponse:
        """사용자 이름 출력"""
        print(User.current_user(request))
        return render(
            request, 
            template_name= OrderView.template_name, 
            context={
            'user': serializeUser(User.current_user(request))
            }
        )
    
class LogoutPageView(View):
    def get(self, request:HttpRequest) -> HttpResponse :
        User.unauthenticate(request)
        return redirect('/login')