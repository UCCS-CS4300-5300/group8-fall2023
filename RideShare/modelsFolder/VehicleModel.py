from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Vehicle(models.Model):
    type = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    isAvailable = models.BooleanField(default=True)
    costPerMinute = models.DecimalField(max_digits=10, decimal_places=2, default=0.50)
    minimumCharge = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)

    class Meta:
        ordering = ['type']

    def __str__(self):
        return f"{self.type} (ID: {self.id})"


class VehicleRental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    checkoutTime = models.DateTimeField(auto_now_add=True)
    checkinTime = models.DateTimeField(null=True, blank=True)
    locations = [
        ('Location1', 'West Lawn'),
        ('Location2', 'Campus Rec Center'),
        ('Location3', 'The Lodge'),
        ('Location4', 'University Hall'),
        ('Location5', 'Location 5'),
    ]
    checkinLocal = models.CharField(max_length=200,
                                    choices=locations, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle.type} - {self.checkoutTime}"

