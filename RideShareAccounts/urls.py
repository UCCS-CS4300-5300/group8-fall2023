from django.contrib import admin
from django.urls import path
from . import views as my_views

urlpatterns = [
    path('signup/', my_views.signuppage, name='signuppage'),
    path('signin/', my_views.signinpage, name='signinpage'),
    path('logout/', my_views.logoutpage, name='logoutpage'),
    path('account/', my_views.accountpage, name='accountpage'),
    path('changepassword/', my_views.changepasswordpage, name='changepasswordpage')
]