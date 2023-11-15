from django.shortcuts import render
from django.views import View
from RideShare.modelsFolder.VehicleModel import Vehicle

class VehicleCheckOut(View):
  template_name = 'vehicleCheckOut.html'
  def get(self, request):
    vehicles = Vehicle.objects.all()

    
    return render(request, self.template_name)