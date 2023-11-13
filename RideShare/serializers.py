from rest_framework import serializers
from RideShare.modelsFolder.VehicleModel import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Vehicle
    fields = ('id', 'type', 'latitude', 'longitude', 'isAvailable')