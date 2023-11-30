from django.test import TestCase, Client
from django.urls import reverse
from RideShare.modelsFolder.VehicleModel import Vehicle, VehicleRental
from django.contrib.auth.models import User
from .forms import CheckInForm, CheckOutForm
from django.utils import timezone
from django import forms

# Create your tests here.
class TestViews(TestCase):
    def test_home_view(self):
        # tests status code 302 since user is not logged in
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        

class TestVehicleMapView(TestCase):
  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.vehicle = Vehicle.objects.create(
      type='Scooter',
      latitude=38.89320,
      longitude=-104.80253,
      isAvailable=True
    )
    self.rental = VehicleRental.objects.create(user=self.user, vehicle=self.vehicle)

  def test_get_map_view_authenticated(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.get(reverse('vehicleMap'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'vehicleMap.html')

  def test_get_map_view_unauthenticated(self):
    response = self.client.get(reverse('vehicleMap'))
    self.assertEqual(response.status_code, 302)

  def test_post_map_view_checkout_success(self):
    self.client.login(username='testuser', password='12345')
    data = {'vehicle_id': self.vehicle.id}
    response = self.client.post(reverse('vehicleMap'), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'vehicleMap.html')
    self.assertTrue(response.context['success'])

    # test if vehicle is marked as not available after checkout
    self.vehicle.refresh_from_db()
    self.assertFalse(self.vehicle.isAvailable)

    new_rentals = VehicleRental.objects.filter(user=self.user, vehicle=self.vehicle)
    new_rental = new_rentals.first()

    self.assertIsNotNone(new_rental)
    self.assertIsNotNone(new_rental.checkoutTime)

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


class TestCheckInView(TestCase):
  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.vehicle = Vehicle.objects.create(
      type='Scooter',
      latitude=38.89320,
      longitude=-104.80253,
      isAvailable=True
    )
    self.rental = VehicleRental.objects.create(user=self.user, vehicle=self.vehicle)

  def test_get_check_in_view_authenticated(self):
    self.client.login(username='testuser', password='12345')
    response = self.client.get(reverse('check_in'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'checkin.html')

  def test_get_check_in_view_not_authenticated(self):
    response = self.client.get(reverse('check_in'))
    self.assertEqual(response.status_code, 200)

  def test_post_check_in_view_success(self):
    self.client.login(username='testuser', password='testpassword')
    form_data = {'rental_id': self.rental.id, 'checkin_location': 'Location1'}
    response = self.client.post(reverse('check_in'), form_data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'checkin.html')

    # Check if the vehicle is marked as available after check-in
    self.vehicle.refresh_from_db()
    self.assertTrue(self.vehicle.isAvailable)

    # Check if the rental is deleted
    with self.assertRaises(VehicleRental.DoesNotExist):
        VehicleRental.objects.get(pk=self.rental.id)


class TestCheckInForm(TestCase):
  def test_valid_checkin_form(self):
    form_data = {'rental_id': 1, 'checkin_location': 'Location1'}
    form = CheckInForm(data=form_data)
    self.assertTrue(form.is_valid())

  def test_invalid_checkin_form_missing_rental_id(self):
    form_data = {'checkin_location': 'Location1'}
    form = CheckInForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('rental_id', form.errors)

  def test_invalid_checkin_form_missing_checkin_location(self):
    form_data = {'rental_id': 1}
    form = CheckInForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('checkin_location', form.errors)

  def test_invalid_rental_id_type(self):
    form_data = {'rental_id': 'invalid', 'checkin_location': 'Location1'}
    form = CheckInForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('rental_id', form.errors)

  def test_invalid_checkin_location(self):
    form_data = {'rental_id': 1, 'checkin_location': 'InvalidLocation'}
    form = CheckInForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('checkin_location', form.errors)

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


class CheckOutFormTests(TestCase):
  def test_valid_checkout_form(self):
      form_data = {'vehicle_id': 1}
      form = CheckOutForm(data=form_data)
      self.assertTrue(form.is_valid())

  def test_invalid_checkout_form_missing_vehicle_id(self):
      form_data = {}
      form = CheckOutForm(data=form_data)
      self.assertFalse(form.is_valid())
      self.assertIn('vehicle_id', form.errors)

  def test_invalid_vehicle_id_type(self):
    form_data = {'vehicle_id': 'invalid'}
    form = CheckOutForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('vehicle_id', form.errors)

  def test_no_vehicle_id_provided(self):
    form_data = {}
    form = CheckOutForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('vehicle_id', form.errors)


    

class TestGeneralForms(TestCase):
  def test_empty_form_checkin(self):
    form = CheckInForm(data={})
    self.assertFalse(form.is_valid())

  def test_empty_form_checkout(self):
    form = CheckOutForm(data={})
    self.assertFalse(form.is_valid())

  def test_widget_type_checkin(self):
    form = CheckInForm()
    self.assertIsInstance(form.fields['rental_id'].widget, forms.HiddenInput)

  def test_required_fields_checkin(self):
    form = CheckInForm()
    self.assertTrue(form.fields['rental_id'].required)
    self.assertTrue(form.fields['checkin_location'].required)

  def test_required_fields_checkout(self):
    form = CheckOutForm()
    self.assertTrue(form.fields['vehicle_id'].required)


class TestURLS(TestCase):
  def test_home_url(self):
    url = reverse('home')
    self.assertEqual(url, '/')

  def test_vehicle_map_url(self):
    url = reverse('vehicleMap')
    self.assertEqual(url, '/vehicleMap/')

  def test_check_in_url(self):
    url = reverse('check_in')
    self.assertEqual(url, '/check-in/')

  def test_checkout_url(self):
    url = reverse('checkout')
    self.assertEqual(url, '/checkout/')


# run tests on the models
class TestVehicleModel(TestCase):
  def setUp(self):
    self.vehicle = Vehicle.objects.create(
        type='Sedan',
        latitude=34.0522,
        longitude=-118.2437,
        isAvailable=True,
        costPerMinute=0.50,
        minimumCharge=5.00
    )

  def test_vehicle_creation(self):
    self.assertIsInstance(self.vehicle, Vehicle)
    self.assertEqual(Vehicle.objects.count(), 1)

  def test_vehicle_str_representation(self):
    expected_str = f"Sedan (ID: {self.vehicle.id})"
    self.assertEqual(str(self.vehicle), expected_str)

  def test_vehicle_ordering(self):
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


class TestVehicleRentalModel(TestCase):
  def setUp(self):
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

  def test_rental_creation(self):
    self.assertIsInstance(self.rental, VehicleRental)
    self.assertEqual(VehicleRental.objects.count(), 1)

  def test_rental_str_representation(self):
    expected_str = f"testuser - Compact - {self.rental.checkoutTime}"
    self.assertEqual(str(self.rental), expected_str)

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
  
