from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('vehicleMap/', views.VehicleMapView.as_view(), name='vehicleMap'),
]