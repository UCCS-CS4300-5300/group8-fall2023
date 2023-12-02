from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from RideShareAccounts.models import PaymentMethod


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", 'password1', 'password2', "email"]

class AccountForm(forms.Form):
    userName = forms.CharField(label='User Name', max_length=200, widget=forms.TextInput())
    userEmail = forms.CharField(label='Email', max_length=200, widget=forms.TextInput())
    defaultPaymentMethod = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), label="Default Payment Method")
