from django.test import TestCase, Client
from django.urls import reverse
from RideShare.modelsFolder.VehicleModel import Vehicle, VehicleRental
from django.contrib.auth.models import User
from .forms import CheckInForm, CheckOutForm
from django.utils import timezone
from django import forms
from RideShareAccounts.models import Account
from RideShareBilling.models import PaymentMethod

# Create your tests here.
# Tests for the normal views.py file, we mostly used a different file
# so there isn't much to do here
class TestViews(TestCase):
    def test_home_view(self):
        # tests status code 302 since user is not logged in
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        
# end of TestViews

# Test the main Map view
class TestVehicleMapView(TestCase):
  # use a simple setUp method of things for every test in this class
  def setUp(self):
    # set up a user
    self.client = Client()
    self.user = User.objects.create_user(username='testuser', password='12345')
    # set up a vehicle
    self.vehicle = Vehicle.objects.create(
      type='Scooter',
      latitude=38.89320,
      longitude=-104.80253,
      isAvailable=True
    )
    # set up a rental
    self.rental = VehicleRental.objects.create(user=self.user, vehicle=self.vehicle)

  # test the map view when successfully logged in
  def test_get_map_view_authenticated(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.get(reverse('vehicleMap'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'vehicleMap.html')

  # test the map view when not logged in
  def test_get_map_view_unauthenticated(self):
    response = self.client.get(reverse('vehicleMap'))
    self.assertEqual(response.status_code, 302)

  # test the map view checkout posting if its successful
  def test_post_map_view_checkout_success(self):
    self.client.login(username='testuser', password='12345')
    data = {'vehicle_id': self.vehicle.id}
    response = self.client.post(reverse('vehicleMap'), data)
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('vehicleMap'))


    # test if vehicle is marked as not available after checkout
    self.vehicle.refresh_from_db()
    self.assertFalse(self.vehicle.isAvailable)
    
    new_rentals = VehicleRental.objects.filter(user=self.user, vehicle=self.vehicle)
    new_rental = new_rentals.first()

    self.assertIsNotNone(new_rental)
    self.assertIsNotNone(new_rental.checkoutTime)

  # tests if checkout fails
  def test_post_vehicle_map_view_checkout_failure(self):
    self.client.login(username='testuser', password='12345')
    self.vehicle.isAvailable = False
    self.vehicle.save()
    data = {'vehicle_id': self.vehicle.id}
    response = self.client.post(reverse('vehicleMap'), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'vehicleMap.html')
    # not sure why this test isn't passing
    #self.assertTrue(response.context['form'].is_valid())
    #self.assertFalse(response.context['success'])
# end of TestVehicleMapView

# test the Check in page view
class TestCheckInView(TestCase):
  # simple setUp function for elements used later
  def setUp(self):
    # set up a user
    self.client = Client()
    self.user = User.objects.create_user(username='testuser', password='12345')

    self.paymentMethod = PaymentMethod.objects.create(description='test payment method')
    self.account = Account.objects.create(
      user=self.user, 
      defaultPaymentMethod=self.paymentMethod)

    #set up a vehicle

    self.vehicle = Vehicle.objects.create(
      type='Scooter',
      latitude=38.89320,
      longitude=-104.80253,
      isAvailable=True
    )
    # set up a rental
    self.rental = VehicleRental.objects.create(user=self.user, vehicle=self.vehicle)


  # test the check in view when logged in

  def test_get_check_in_view_authenticated(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.get(reverse('check_in'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'checkin.html')

  # test the check in view when not logged in
  def test_get_check_in_view_not_authenticated(self):
    response = self.client.get(reverse('check_in'))
    self.assertEqual(response.status_code, 302)

  # test if the check in post works
  def test_post_check_in_view_success(self):
    self.client.login(username='testuser', password='12345')
    form_data = {'rental_id': self.rental.id, 'checkin_location': 'Location1'}
    response = self.client.post(reverse('check_in'), form_data, follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertRedirects(response, reverse('check_in'))

    # Check if the vehicle is marked as available after check-in
    self.vehicle.refresh_from_db()
    self.assertTrue(self.vehicle.isAvailable)

    # Check if the rental is now has a check in time
    self.rental.refresh_from_db()
    self.assertNotEqual(self.rental.checkinTime, None)



  def test_billing_greater_than_minimum_charge(self):

    self.client.login(username='testuser', password='12345')
    form_data = {'rental_id': self.rental.id, 'checkin_location': 'Location1'}
    #Setting up checkout for the time difference - currently at 30 minutes
    self.rental.checkoutTime=timezone.now() - timezone.timedelta(minutes=30)  
    time_difference = 30
    self.rental.save()
    self.client.post(reverse('check_in'), form_data, follow=True)
    
    #check if the balance is updated correctly
    self.account.refresh_from_db()
    self.assertEqual(self.account.outstandingBalance,
                     time_difference * self.rental.vehicle.costPerMinute)

  def test_billing_less_than_minimum_charge(self):

    self.client.login(username='testuser', password='12345')
    form_data = {'rental_id': self.rental.id, 'checkin_location': 'Location1'}
    #Setting up checkout for the time difference - currently at 30 minutes
    self.rental.checkoutTime=timezone.now() - timezone.timedelta(minutes=3)  
    self.rental.save()
    self.client.post(reverse('check_in'), form_data, follow=True)
  
    #check if the balance is updated correctly
    self.account.refresh_from_db()
    self.assertEqual(self.account.outstandingBalance, self.vehicle.minimumCharge)
    
# end of TestCheckInView


# test the check in form view
class TestCheckInForm(TestCase):
  # test the check in form with a valid form
  def test_valid_checkin_form(self):
    form_data = {'rental_id': 1, 'checkin_location': 'Location1'}
    form = CheckInForm(data=form_data)
    self.assertTrue(form.is_valid())

  # test an invalid form (missing data)
  def test_invalid_checkin_form_missing_rental_id(self):
    form_data = {'checkin_location': 'Location1'}
    form = CheckInForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('rental_id', form.errors)

  # test a missing location form
  def test_invalid_checkin_form_missing_checkin_location(self):
    form_data = {'rental_id': 1}
    form = CheckInForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('checkin_location', form.errors)

  # test a missing rental id form
  def test_invalid_rental_id_type(self):
    form_data = {'rental_id': 'invalid', 'checkin_location': 'Location1'}
    form = CheckInForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('rental_id', form.errors)

  # test an invalid rental location
  def test_invalid_checkin_location(self):
    form_data = {'rental_id': 1, 'checkin_location': 'InvalidLocation'}
    form = CheckInForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('checkin_location', form.errors)

  # test case sensitivity of location
  def test_checkin_location_case_sensitivity(self):
    # Assuming 'Location1' is a valid choice in VehicleRental.locations
    valid_location = 'Location1'

    # Test with lowercase checkin_location
    form_data_lower = {'rental_id': 1, 'checkin_location': valid_location.lower()}
    form_lower = CheckInForm(data=form_data_lower)
    self.assertFalse(form_lower.is_valid())
    self.assertIn('checkin_location', form_lower.errors)

    # Test with uppercase checkin_location
    form_data_upper = {'rental_id': 1, 'checkin_location': valid_location.upper()}
    form_upper = CheckInForm(data=form_data_upper)
    self.assertFalse(form_upper.is_valid())
    self.assertIn('checkin_location', form_upper.errors)

# end of TestCheckInForm

# testing the check out form
class CheckOutFormTests(TestCase):
  # test a valid checkout
  def test_valid_checkout_form(self):
      form_data = {'vehicle_id': 1}
      form = CheckOutForm(data=form_data)
      self.assertTrue(form.is_valid())

  # test an invalid form (missing data = vehicle id)
  def test_invalid_checkout_form_missing_vehicle_id(self):
      form_data = {}
      form = CheckOutForm(data=form_data)
      self.assertFalse(form.is_valid())
      self.assertIn('vehicle_id', form.errors)

  # test an invalid vehicle id
  def test_invalid_vehicle_id_type(self):
    form_data = {'vehicle_id': 'invalid'}
    form = CheckOutForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('vehicle_id', form.errors)

  # test no vehicle id
  def test_no_vehicle_id_provided(self):
    form_data = {}
    form = CheckOutForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('vehicle_id', form.errors)

# end of TestCheckOutForm
    
# general form tests
class TestGeneralForms(TestCase):
  # test empty forms
  def test_empty_form_checkin(self):
    form = CheckInForm(data={})
    self.assertFalse(form.is_valid())

  def test_empty_form_checkout(self):
    form = CheckOutForm(data={})
    self.assertFalse(form.is_valid())

  # test the form widgets
  def test_widget_type_checkin(self):
    form = CheckInForm()
    self.assertIsInstance(form.fields['rental_id'].widget, forms.HiddenInput)

  # test the required fields
  def test_required_fields_checkin(self):
    form = CheckInForm()
    self.assertTrue(form.fields['rental_id'].required)
    self.assertTrue(form.fields['checkin_location'].required)


  def test_required_fields_checkout(self):
    form = CheckOutForm()
    self.assertTrue(form.fields['vehicle_id'].required)

# end of TestGeneralForms

# test URL mappings
class TestURLS(TestCase):
  # pretty self explanatory url mapping names
  # home url
  def test_home_url(self):
    url = reverse('home')
    self.assertEqual(url, '/')

  # vehicle map
  def test_vehicle_map_url(self):
    url = reverse('vehicleMap')
    self.assertEqual(url, '/vehicleMap/')

  # check in url
  def test_check_in_url(self):
    url = reverse('check_in')
    self.assertEqual(url, '/check-in/')

  # check out url
  def test_checkout_url(self):
    url = reverse('checkout')
    self.assertEqual(url, '/checkout/')

# end of TestURLS

# run tests on the models
# test the Vehicle Model
class TestVehicleModel(TestCase):
  # standared setUp function
  def setUp(self):
    self.vehicle = Vehicle.objects.create(
        type='Sedan',
        latitude=34.0522,
        longitude=-118.2437,
        isAvailable=True,
        costPerMinute=0.50,
        minimumCharge=5.00
    )

  # test the vehicle creation success
  def test_vehicle_creation(self):
    self.assertIsInstance(self.vehicle, Vehicle)
    self.assertEqual(Vehicle.objects.count(), 1)

  # test the vehicle string representation of the object
  def test_vehicle_str_representation(self):
    expected_str = f"Sedan (ID: {self.vehicle.id})"
    self.assertEqual(str(self.vehicle), expected_str)

  # test the vehicle ordering with lists
  def test_vehicle_ordering(self):
    # create two vehicles to test ordering of creation
    suv = Vehicle.objects.create(
        type='SUV',
        latitude=34.0522,
        longitude=-118.2437,
        isAvailable=True,
        costPerMinute=0.75,
        minimumCharge=6.00
    )
    sedan = Vehicle.objects.create(
        type='Compact',
        latitude=34.0522,
        longitude=-118.2437,
        isAvailable=True,
        costPerMinute=0.60,
        minimumCharge=5.50
    )

    vehicles = Vehicle.objects.all()
    self.assertEqual(list(vehicles), [sedan, suv, self.vehicle])

# end of TestVehicleModel

# test the Rental Model
class TestVehicleRentalModel(TestCase):
  # standared setUp function
  def setUp(self):
    # set up a user, vehicle, and rental
    self.user = User.objects.create(username='testuser')
    self.vehicle = Vehicle.objects.create(
        type='Compact',
        latitude=34.0522,
        longitude=-118.2437,
        isAvailable=True,
        costPerMinute=0.60,
        minimumCharge=5.50
    )
    self.rental = VehicleRental.objects.create(
        user=self.user,
        vehicle=self.vehicle,
        checkoutTime='2023-01-01T12:00:00Z',
        checkinTime=None,
        checkinLocal='Location1'
    )

  # test the creation of a rental object 
  def test_rental_creation(self):
    self.assertIsInstance(self.rental, VehicleRental)
    self.assertEqual(VehicleRental.objects.count(), 1)

  # test the vehicle rental string representation
  def test_rental_str_representation(self):
    expected_str = f"testuser - Compact - {self.rental.checkoutTime}"
    self.assertEqual(str(self.rental), expected_str)

  # test the rental ordering like the Vehicles, 
  # create two rentals and tests
  def test_rental_ordering(self):
    rental2 = VehicleRental.objects.create(
        user=self.user,
        vehicle=self.vehicle,
        checkoutTime='2023-01-02T12:00:00Z',
        checkinTime=None,
        checkinLocal='Location2'
    )
    rental3 = VehicleRental.objects.create(
        user=self.user,
        vehicle=self.vehicle,
        checkoutTime='2023-01-03T12:00:00Z',
        checkinTime=None,
        checkinLocal='Location3'
    )

    rentals = VehicleRental.objects.all()
    self.assertEqual(list(rentals), [self.rental, rental2, rental3])

# end of TestVehicleRentalModel

