from django.shortcuts import render
from django.views import View

# Create your views here.


def home(request):
  context = {}
  return render(request, 'home.html', context)

class VehicleMapView(View):
  template_name = 'vehicleMap.html'

  def get(self, request):
    context = {}
    context['key'] = 'AIzaSyD-oTBt9sdMhCXyQqrtuok0CYvP7ev58hg'
      
    return render(request, self.template_name, context)  