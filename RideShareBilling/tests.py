from django.test import TestCase
from .models import PaymentMethod, Payment
from django.contrib.auth.models import User

# Create your tests here.
class TestPaymentMethodModel(TestCase):
  def test_payment_method_creation(self):
    payment_method = PaymentMethod(description="Paypal Payment Method")
    self.assertEqual(payment_method.description, 'Paypal Payment Method')

  def test_payment_method_ordering(self):
    payment_method1 = PaymentMethod.objects.create(description='Payment Method 1')
    payment_method2 = PaymentMethod.objects.create(description='Payment Method 2')
    ordered_payment_methods = list(PaymentMethod.objects.all())

    self.assertEqual(ordered_payment_methods, [payment_method1, payment_method2])


class TestPaymentModel(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    self.payment_method = PaymentMethod.objects.create(description='Test Payment Method')


  def test_create_payment(self):
    payment = Payment.objects.create(user=self.user, paymentMethod=self.payment_method, amountPaid=50.00)
    self.assertEqual(payment.user, self.user)
    self.assertEqual(payment.paymentMethod, self.payment_method)
    self.assertEqual(payment.amountPaid, 50.00)

  def test_payment_ordering(self):
    user1 = User.objects.create_user(username='user1', password='password1')
    user2 = User.objects.create_user(username='user2', password='password2')

    payment1 = Payment.objects.create(user=user1, paymentMethod=self.payment_method, amountPaid=30.00)
    payment2 = Payment.objects.create(user=user2, paymentMethod=self.payment_method, amountPaid=20.00)

    ordered_payments = list(Payment.objects.all())
    self.assertEqual(ordered_payments, [payment1, payment2])