from django.contrib import admin
from django.urls import path
from . import views as my_views

urlpatterns = [
    path('signup/', my_views.signuppage, name='signuppage'),
    path('signin/', my_views.signinpage, name='signinpage')
]