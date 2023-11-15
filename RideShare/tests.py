from django.test import TestCase, Client
from django.urls import reverse
from RideShare.modelsFolder.VehicleModel import Vehicle, VehicleRental
from django.contrib.auth.models import User
from .forms import CheckInForm
from django.utils import timezone

# Create your tests here.
class TestViews(TestCase):
    def test_home_view(self):
        # tests status code 302 since user is not logged in
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        

class TestVehicleMapView(TestCase):
  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    Vehicle.objects.create(type='Scooter', latitude=37.123, longitude=-122.456, isAvailable=True)
    Vehicle.objects.create(type='Car', latitude=38.456, longitude=-123.789, isAvailable=False)
    
    
  def test_vehicle_map_view(self):
    self.client.login(username='testuser', password='testpassword')
    response = self.client.get(reverse('vehicleMap'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'vehicleMap.html')

    self.assertIn('key', response.context)
    self.assertIn('vehicles', response.context)
    self.assertIn('response_data', response.context)

    self.assertContains(response, 'Scooter')
    self.assertContains(response, 'Car')
    self.assertContains(response, 'AIzaSyD-oTBt9sdMhCXyQqrtuok0CYvP7ev58hg')
    self.assertContains(response, '37.123')
    self.assertContains(response, '-122.456')
    self.assertContains(response, '38.456')
    self.assertContains(response, '-123.789')

  def test_map_unauthenticated_user(self):
    response = self.client.get(reverse('vehicleMap'))
    self.assertEqual(response.status_code, 302)


class TestCheckInView(TestCase):
  def setUp(self):
    self.client = Client()
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    self.vehicle = Vehicle.objects.create(type='Scooter', latitude=37.123, longitude=-122.456, isAvailable=True)
    self.rental = VehicleRental.objects.create(user=self.user, vehicle=self.vehicle)

  def test_get_checkin_view_valid_form(self):
    self.client.login(username='testuser', password='testpassword')
    response = self.client.get(reverse('check_in'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'checkin.html')
    self.assertIsInstance(response.context['form'], CheckInForm)

  def test_post_checkin_view(self):
    self.client.login(username='testuser', password='testpassword')
    data = {'vehicle_id': self.vehicle.id, 'checkin_location': 'Location1'}
    response = self.client.post(reverse('check_in'), data)
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('vehicleMap'))
    rental = VehicleRental.objects.get(id=self.rental.id)

    self.assertIsNotNone(rental.checkinTime)
    self.assertEqual(rental.checkinLocal, 'Location1')
    self.assertTrue(rental.vehicle.isAvailable)

  def test_post_checkin_view_invalid_form(self):
    self.client.login(username='testuser', password='testpassword')
    data = {}
    response = self.client.post(reverse('check_in'), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'checkin.html')
    self.assertIn('form', response.context)
    self.assertFalse(response.context['form'].is_valid())

  def test_post_checkin_view_invalid_rental(self):
    self.client.login(username='testuser', password='testpassword')
    data = {'vehicle_id': self.vehicle.id, 'checkin_location': 'Location1'}
    self.rental.delete()
    
    response = self.client.post(reverse('check_in'), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'checkin.html')
    self.assertIn('form', response.context)

    
    # self.assertFalse(response.context['form'].is_valid())


class TestCheckInForm(TestCase):
  def setUp(self):
    self.valid_data = {'vehicle_id': 1, 'checkin_location': 'Location1'}

  def test_valid_form(self):
    form = CheckInForm(data=self.valid_data)
    self.assertTrue(form.is_valid())

  def test_empty_form(self):
    form = CheckInForm(data={})
    self.assertFalse(form.is_valid())
    self.assertIn('vehicle_id', form.errors)
    self.assertIn('checkin_location', form.errors)

  def test_missing_vehicle_id(self):
    data = self.valid_data.copy()
    del data['vehicle_id']
    form = CheckInForm(data=data)
    self.assertFalse(form.is_valid())
    self.assertIn('vehicle_id', form.errors)

  def test_missing_checkin_location(self):
    data = self.valid_data.copy()
    del data['checkin_location']
    form = CheckInForm(data=data)
    self.assertFalse(form.is_valid())
    self.assertIn('checkin_location', form.errors)

  def test_invalid_vehicle_id(self):
    data = self.valid_data.copy()
    data['vehicle_id'] = 'invalid_id'
    form = CheckInForm(data=data)
    self.assertFalse(form.is_valid())
    self.assertIn('vehicle_id', form.errors)

  def test_invalid_checkin_location(self):
    data = self.valid_data.copy()
    data['checkin_location'] = 'InvalidLocation'
    form = CheckInForm(data=data)
    self.assertFalse(form.is_valid())
    self.assertIn('checkin_location', form.errors)

  def test_choices_for_checkin_location(self):
    form = CheckInForm()
    choices = form.fields['checkin_location'].choices
    expected_choices = VehicleRental.locations
    self.assertEqual(choices, expected_choices)

    
    
    
    
    
