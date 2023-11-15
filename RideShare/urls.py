from django.urls import path
from . import views
from RideShare.viewFolder.VehicleMapView import VehicleMapView
from RideShare.viewFolder.VehicleCheckOut import VehicleCheckOut

urlpatterns = [
  path('', views.home, name='home'),
  path('vehicleMap/', VehicleMapView.as_view(), name='vehicleMap'),
  path('vehicleCheckOut/', VehicleCheckOut.as_view(), name='vehicleCheckOut')
]