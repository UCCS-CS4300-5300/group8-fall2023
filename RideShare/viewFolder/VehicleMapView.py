from django.shortcuts import render, redirect
from django.views import View
from RideShare.modelsFolder.VehicleModel import Vehicle
from RideShare.modelsFolder.VehicleModel import VehicleRental
from RideShare.forms import CheckInForm, CheckOutForm
from django.utils import timezone


class VehicleMapView(View):
  template_name = 'vehicleMap.html'

  def get(self, request):

    if not request.user.is_authenticated:
      return redirect('/signin')
    
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
    context['vehicle'] = Vehicle.objects.first()

    return render(request, self.template_name, context)  

#Check Out
  def post(self, request):
    form = CheckOutForm(request.POST)
  
    if form.is_valid():
      vehicle_id = form.cleaned_data['vehicle_id']
      vehicle = Vehicle.objects.get(id=vehicle_id)
      if vehicle.isAvailable:
        vehicle.isAvailable = False
        vehicle.save()
  
        rental = VehicleRental.objects.create(user=request.user, vehicle=vehicle)
        return render(request, 'checkoutSuccess.html', {'form': form, 'success': True})
  
    vehicles = Vehicle.objects.filter(isAvailable=True)
    return render(request, self.template_name, {'form': form, 'vehicles': vehicles})



# David - gave up on check in with post function in MapView
class CheckInView(View):
  template_name = "checkin.html"

  def get(self, request):
    form = CheckInForm()

    # fetch users current vehicles that are not checked in
    rentals = VehicleRental.objects.filter(user=request.user, checkinTime__isnull=True)

    return render(request, self.template_name, {'form': form, 'rentals': rentals})

  def post(self, request):
    form = CheckInForm(request.POST)
    print("Form data: ", request.POST)
    
    rentals = VehicleRental.objects.filter(user=request.user, checkinTime__isnull=True)
    print("before if form is valid")
    if form.is_valid():
      print("in is_valid")
      # print(f"Rental ID: {form.cleaned_data['rental_id']}")
      rental_id = form.request.POST.get('rental_id')
      vehicle_id = form.request.POST.get('vehicle_id')
      # checkin_location = form.cleaned_data['checkin_location']


      #rentalObject

      print("Hello there, before try-except")
      try:
        # Update the availability of the vehicle
        print("after try-except")
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        vehicle.isAvailable = True
        vehicle.save()
        
        rental = VehicleRental.objects.get(pk=rental_id, user=request.user, checkinTime__isnull=True)

        # rental.checkin_location = checkin_location
        rental.checkin_time = timezone.now()
        rental.save()
        # rental.delete()
        return render(request, 'checkinSuccess.html', {'form': form, 'success': True, 'rentals': rentals})
      except (Vehicle.DoesNotExist, VehicleRental.DoesNotExist):

        return render(request, self.template_name) 


        

    # handle invalid form data
    
    print("form errors: ", form.errors.as_data())

    
    return render(request, self.template_name, {'form': form, 'rentals': rentals})



  

