from django.test import TestCase
from django.urls import reverse
from RideShare.modelsFolder.VehicleModel import Vehicle

# Create your tests here.
class TestViews(TestCase):
    def test_home_view(self):
        # tests status code 302 since user is not logged in
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

class TestVehicleMapView(TestCase):
  def setUp(self):
    Vehicle.objects.create(type='Scooter', latitude=37.123, longitude=-122.456, isAvailable=True)
    Vehicle.objects.create(type='Car', latitude=38.456, longitude=-123.789, isAvailable=False)
    
  def test_vehicle_map_view(self):
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
    
