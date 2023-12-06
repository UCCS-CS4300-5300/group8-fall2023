from django.db import models
from django.contrib.auth.models import User


class PaymentMethod(models.Model):
    description = models.CharField(max_length=50)

    class Meta:
        ordering = ['id']


class Payment(models.Model):
    """
    This form extends the Default user creation form.  It adds in default payment method in the template
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)
    amountPaid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timePaid = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
