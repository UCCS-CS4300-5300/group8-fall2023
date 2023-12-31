from django.db import models
from django.contrib.auth.models import User
from RideShareBilling.models import PaymentMethod


class Account(models.Model):
    """
    This is the model for an account.  This basically adds some additional fields to the user object.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outstandingBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    defaultPaymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['user']
