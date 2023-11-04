from django.db import models

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