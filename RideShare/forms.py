from django import forms
from RideShare.modelsFolder.VehicleModel import Vehicle, VehicleRental

class CheckInForm(forms.Form):
  rental_id = forms.IntegerField()
  vehicle_id = forms.IntegerField()
  # checkin_location = forms.ChoiceField(choices=VehicleRental.locations, label='Check-in Location')
  
class CheckOutForm(forms.Form):
  vehicle_id = forms.IntegerField(widget=forms.HiddenInput())