from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserBillingAccount(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  amountDue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  paymentMethod = models.CharField(max_length=50, default = "Credit Card")

  class Meta:
    ordering = ['user']
    
  def __str__(self):
    return self.user.username + " UBA"