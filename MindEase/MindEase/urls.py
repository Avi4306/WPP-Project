"""
URL configuration for MindEase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from MindEase import views
# urlpatterns = from django.urls import path
# from . import views
# from django.contrib import admin

urlpatterns = [
    path('', views.index,name='home'),
    path('admin/', admin.site.urls),
    path('conditions/',views.conditions,name='cond'),
    path('appointment/', views.appointment,name='appoi'),
    path('funzone/', views.funzone,name='fun'),
    path('psychoeducation/', views.psychoeducation,name='psychoedu'),
    path('appointment/redirect/', views.redirect,name='redirect'),
    path('resources', views.resources,name='resources'),
    path('signup/', views.signupPage, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('terms-and-conditions/', views.terms, name='terms'),
    path('terms-and-conditions/privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
