from django.shortcuts import render, redirect
from django.views import View
from RideShare.modelsFolder.VehicleModel import Vehicle
from RideShare.modelsFolder.VehicleModel import VehicleRental
from RideShare.forms import CheckInForm, CheckOutForm
from django.utils import timezone
import decimal
from RideShareAccounts.models import Account

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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

        #With how post works, you need to redirect to the same page so that 
        #it recieves a GET request
        #in order to do that you need redirect, but you cant pass in 'vehicleMap', you need to
        #pass in a variable that holds 'vehicleMap'
        redirectView = 'vehicleMap'
        return redirect(redirectView)
        #return render(request, self.template_name, {'form': form, 'success': True})

  
    vehicles = Vehicle.objects.filter(isAvailable=True)
    return render(request, self.template_name, {'form': form, 'vehicles': vehicles})
    

# Check in View
@method_decorator(login_required, name='dispatch')
class CheckInView(View):
  template_name = "checkin.html"

  def get(self, request):
    form = CheckInForm()
    context = {
      'form': form,
      'key': 'AIzaSyD-oTBt9sdMhCXyQqrtuok0CYvP7ev58hg',
      'rentals': VehicleRental.objects.filter(user=request.user, checkinTime__isnull=True),
      }
    return render(request, self.template_name, context)

  def post(self, request):
    form = CheckInForm(request.POST)
    if form.is_valid():
      rental_id = form.cleaned_data['rental_id']
      checkin_location = form.cleaned_data['checkin_location']
      

 
      
      #rentalObject
      
      
      # Update the availability of the vehicle
      vehicle_id = VehicleRental.objects.get(id=rental_id).vehicle.id
      account = Account.objects.get(user=request.user)
      vehicle = Vehicle.objects.get(pk=vehicle_id)
      vehicle.isAvailable = True
      vehicle.save()
      
      rental = VehicleRental.objects.get(pk=rental_id)

      rental.checkin_location = checkin_location
      rental.checkinTime = timezone.now()
      rental.save()
  

      #calculate the time in minutes flooring to the last full minute
      timeDiff = rental.checkinTime - rental.checkoutTime
      rentalCost = (timeDiff.total_seconds() // 60)
      rentalCost = decimal.Decimal(rentalCost) * rental.vehicle.costPerMinute
      #make sure that minimumCharge is made
      if rentalCost < rental.vehicle.minimumCharge:
        rentalCost = rental.vehicle.minimumCharge
      
      account.outstandingBalance += rentalCost
      account.save()

      
      redirectView = 'check_in'

      return redirect(redirectView)


      # handle invalid form data
    context = {
      'form': form,
      'key': 'AIzaSyD-oTBt9sdMhCXyQqrtuok0CYvP7ev58hg',
      'vehicles': Vehicle.objects.all(),
      'rentals': VehicleRental.objects.filter(user=request.user, checkinTime__isnull=True),
      }
    
    print("form errors: ", form.errors)
    print("Redirecting to 'vehicle_map' failed. Form is not valid or rental is not found.")
    return render(request, self.template_name, context)


  

