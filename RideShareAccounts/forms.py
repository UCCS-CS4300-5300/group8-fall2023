from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from RideShareAccounts.models import PaymentMethod


class SignUpForm(UserCreationForm):
    """
    This form extends the Default user creation form.  It adds in default payment method in the template.
    """

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class AccountForm(forms.Form):
    """
    This is a custom form for updating an account.
    """

    userName = forms.CharField(label='User Name', max_length=200, widget=forms.TextInput())
    userEmail = forms.CharField(label='Email', max_length=200, widget=forms.TextInput())
    defaultPaymentMethod = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), label="Default Payment Method")


class ChangePasswordForm(PasswordChangeForm):
    """
    This form extends the Default change password form.  It allows us to style the form better.
    """

    class Meta:
        model = User
        fields = ['oldpassword', 'newpassword1', 'newpassword2']
