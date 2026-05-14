"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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


from django.urls import path

from . import views
from django.contrib import admin


urlpatterns = [
   path('register/',views.register, name='register'),
   path('login/',views.login, name='login'),
   path('logout/',views.logout, name='logout'),
   path('profile/',views.profile, name='profile'),
   path('activate/<uidb64>/<token>/', views.activate, name="activate"),
   path('forgotpassword/', views.forgot_password, name='forgot_password'),
   path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
   path('edit-profile/', views.User_profile, name='edit_profile'),
   path('change-password/', views.change_password, name='change_password'),
   path('order_details/<str:order_number>/', views.Order_details, name='order_details'),
]

