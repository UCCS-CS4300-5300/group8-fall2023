from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Vehicle(models.Model):
  type = models.CharField(max_length=200)
  latitude =  models.FloatField()
  longitude = models.FloatField()
  isAvailable = models.BooleanField(default=True)

  class Meta:
    ordering = ['type']

  def __str__(self):
    return self.type + str(self.id)

# random comment test
class VehicleRental(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
  checkoutTime = models.DateTimeField(auto_now_add=True)
  checkinTime = models.DateTimeField(null=True, blank=True)
  locations = [
    ('Location1', 'Location 1'),
    ('Location2', 'Location 2'),
    ('Location3', 'Location 3'),
    ('Location4', 'Location 4'),
    ('Location5', 'Location 5'),
  ]
  checkinLocal = models.CharField(max_length=200, choices=locations, null=True, blank=True)
  paymentMethod = models.CharField(max_length=200)

  def __str__(self):
    return f"{self.user.username} - {self.vehicle.type} - {self.checkout_time}"
