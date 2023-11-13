from django.shortcuts import render
from django.views import View
from RideShare.modelsFolder.VehicleModel import Vehicle
#from RideShare.serializers import VehicleSerializer

class VehicleMapView(View):
  template_name = 'vehicleMap.html'

  def get(self, request):
    context = {}

    vehicles = Vehicle.objects.all()

    """"
    serializers is not working because djangorestframework package will not install
    serialized_data = [
      VehicleSerializer(vehicle).data for vehicle in vehicles
    ]
    """

    serialized_data = [
      {"id": vehicle.id, 
       "type": vehicle.type, 
       "latitude": vehicle.latitude,
       "longitude": vehicle.longitude,
       # note that booleans have to be converted to strings for JSON.parse
       "isAvailable": str("{}").format(vehicle.isAvailable)
      } 
      for vehicle in vehicles
    ]

    response_data = {
      'count': len(serialized_data),
      'results': serialized_data
    }

    context['key'] = 'AIzaSyD-oTBt9sdMhCXyQqrtuok0CYvP7ev58hg'
    context['vehicles'] = vehicles
    context['response_data'] = response_data

    return render(request, self.template_name, context)  