from django.urls import path
from . import views
from RideShare.viewFolder.VehicleMapView import VehicleMapView

urlpatterns = [
  path('', views.home, name='home'),
  path('vehicleMap/', VehicleMapView.as_view(), name='vehicleMap')
]