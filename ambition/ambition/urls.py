"""ambition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from store.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/email/validation', csrf_exempt(EmailValidationView.as_view())),
    path('api/v1/signup', csrf_exempt(UserCreateView.as_view())),
    path('api/v1/login', csrf_exempt(UserLoginView.as_view())),
    path('api/v1/logout', csrf_exempt(UserLogoutView.as_view())),
    path('api/v1/order', csrf_exempt(OrderView.as_view())),
    path('api/v1/order/<int:order_id>', csrf_exempt(OrderIdView.as_view())),
    path('api/v1/product', csrf_exempt(ProductView.as_view())),
    path('api/v1/product/<int:product_id>', csrf_exempt(ProductIdView.as_view())),
    path('api/v1/category', csrf_exempt(CategoryView.as_view())),
    path('login', TemplateView.as_view(template_name='login_view.html')),
    path('signup', TemplateView.as_view(template_name='signup_view.html')),
    path('manage', TemplateView.as_view(template_name='manage_view.html')),
    path('manage/order', TemplateView.as_view(template_name='ordermenu.html')),
    path('manage/menu', TemplateView.as_view(template_name='menu.html')),
    path('manage/sales', TemplateView.as_view(template_name='manage.html')),
    path('m/home', TemplateView.as_view(template_name='moblie-view/main.html')),
    path('m/menu', TemplateView.as_view(template_name="mobile-view/menu.html")),
    path('m/receipt', TemplateView.as_view(template_name="mobile-view/receipt.html")),
]
