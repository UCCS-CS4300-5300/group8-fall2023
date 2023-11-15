from django.urls import path
from . import views
from RideShare.viewFolder.VehicleMapView import VehicleMapView, CheckInView

urlpatterns = [
  path('', views.home, name='home'),
  path('vehicleMap/', VehicleMapView.as_view(), name='vehicleMap'),
  path('check-in/', CheckInView.as_view(), name='check_in'),
]