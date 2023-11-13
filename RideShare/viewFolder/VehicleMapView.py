from django.shortcuts import render, redirect
from django.views import View
from RideShare.modelsFolder.VehicleModel import Vehicle
from RideShare.modelsFolder.VehicleModel import VehicleRental
from django.urls import reverse
from RideShare.forms import CheckInForm


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
    context['rentals'] = VehicleRental.objects.filter(user=request.user, checkinTime__isnull=True)

    return render(request, self.template_name, context)  


  
  def post(self, request):
    form = CheckInForm(request.POST)
    if form.is_valid():
      vehicle_id = form.cleaned_data['vehicle_id']
      checkin_location = form.cleaned_data['checkin_location']
      
      vehicle = Vehicle.objects.get(pk=vehicle_id)
      rental = VehicleRental.objects.filter(user=request.user, vehicle=vehicle, checkinTime__isnull=True).first()

      if rental: 
        rental.checkin_location = checkin_location
        rental.payment_method = payment_method
        rental.checkin_time = timezone.now()
        rental.save()

        # Update the availability of the vehicle
        vehicle.is_available = True
        vehicle.save()

        return redirect('vehicle_map')

      # handle invalid form data
    context = {
      'form': form,
      'key': 'AIzaSyD-oTBt9sdMhCXyQqrtuok0CYvP7ev58hg',
      'vehicles': Vehicle.objects.all(),
      'rentals': VehicleRental.objects.filter(user=request.user, checkinTime__isnull=True),
      }
    return render(request, self.template_name, context)