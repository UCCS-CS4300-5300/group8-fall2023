from django.contrib import admin
from django.urls import path
from . import views
from RideShare.sign_up_sign_in import sign_up_view

urlpatterns = [
  path('', views.home, name='home'),
  path('signup', sign_up_view.signuppage, name='signup'),
]