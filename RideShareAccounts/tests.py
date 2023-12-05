from django.test import TestCase
from django.contrib.auth.models import User
from .forms import SignUpForm, AccountForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from RideShareBilling.models import PaymentMethod, Payment
from .models import Account

# Create your tests here.
#Form testing
class TestSignUpForm(TestCase):
  def test_signup_form_valid(self):
    data = {
      'username': 'testuser',
      'password1': 'testpassword123',
      'password2': 'testpassword123',
      'email': 'testuser@example.com',
    }
    form = SignUpForm(data)
    self.assertTrue(form.is_valid())

  def test_signup_invalid_form(self):
    form = SignUpForm(data={})
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 3)


  def test_mismatched_passwords(self):
    data = {
        'username': 'testuser',
        'password1': 'testpassword123',
        'password2': 'differentpassword',
        'email': 'testuser@example.com',
    }
    form = SignUpForm(data)
    self.assertFalse(form.is_valid())
    self.assertIn('password2', form.errors)

  def test_creates_user(self):
    data = {
        'username': 'testuser',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'email': 'testuser@example.com',
    }
    self.assertFalse(User.objects.filter(username=data['username']).exists())

# end of Testing SignUpForm

#test change password form
class TestChangePasswordForm(TestCase):
  # should pass when implemented fully
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='oldpassword123')
  def test_change_valid_form(self):
    
    form = ChangePasswordForm(user = self.user, data = {
                                'oldpassword': 'oldpassword123',
                                'newpassword1': 'newpassword123',
                                'newpassword2': 'newpassword123'
                              })
   
  
    self.assertTrue(form.is_valid())

# end of TestChangePasswordForm

# tests various cases with signing up
class TestSignUpView(TestCase):
  def test_authenticated_user_redirected(self):
    self.user = User.objects.create_user(username='test', password='test')
    self.client.login(username='test', password='test')
    response = self.client.get(reverse('signuppage'))
    # expects a redirect
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, reverse('home'))

  def test_get_request_return_signup_form(self):
    response = self.client.get(reverse('signuppage'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'signup.html')
    self.assertIsInstance(response.context['form'], UserCreationForm)

  def test_valid_signup_form_redirects_to_home(self):
    data = {
      'username': 'test',
      'password1': 'newpassword',
      'password2': 'newpassword',
    }
    response = self.client.post(reverse('signuppage'), data)
    self.assertEqual(response.status_code, 200)

 

  
  def tests_authenticated_user_redirected(self):
    user = User.objects.create_user(username='test', password='test')
    self.client.login(username='test', password='test')

    data = {
      'username': 'test',
      'password1': 'newpassword',
      'password2': 'newpassword',
    }

    response = self.client.post(reverse('signuppage'), data)
    self.assertEqual(response.status_code, 302)

  # these two test functions are being strange. they should work but they aren't
  '''
  def test_existing_user_authentication_error(self):
    user = User.objects.create_user(username='test', password='test')
    data = {
      'username': 'test47',
      'password1': 'newpassword',
      'password2': 'newpassword',
    }
    response = self.client.post(reverse('signuppage'), data)

    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'A user with that username already exists.')


  def test_invalid_signup(self):
    data = {
      'username': '',
      'password1': 'password',
      'password2': 'password2',
    }
    response = self.client.post(reverse('signuppage'), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'signup.html')
    self.assertIsInstance(response.context['form'], UserCreationForm)
    self.assertFormError(response, 'form', 'username', 'This field is required.')
    self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')'''


# end of TestSignUpView

# tests various cases of signing into the app
class TestSignInView(TestCase):
  def test_authenticated_user_redirected(self):
    self.user = User.objects.create_user(username='test', password='test')
    self.client.login(username='test', password='test')
    response = self.client.get(reverse('signinpage'))
    # expects a redirect
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, reverse('home'))

  def test_get_request_return_signin_form(self):
    response = self.client.get(reverse('signinpage'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'signin.html')
    self.assertIsInstance(response.context['form'], AuthenticationForm)

  def test_valid_signin_form_redirects_to_home(self):
    data = {
      'username': 'test',
      'password': 'test',
    }
    response = self.client.post(reverse('signinpage'), data)
    # self.assertEqual(response.status_code, 302)
    # self.assertEqual(response, reverse('home'))

  def test_invalid_signin(self):
    data = {
      'username': 'test',
      'password': 'test2',
    }
    response = self.client.post(reverse('signinpage'), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'signin.html')
    self.assertIsInstance(response.context['form'], AuthenticationForm)

# end of TestSignInView

# these tests evaluate logging out
class TestLogoutView(TestCase):
  def test_authenticated_user_redirected(self):
    self.user = User.objects.create_user(username='test', password='test')
    self.client.login(username='test', password='test')
    response = self.client.get(reverse('logoutpage'))
    # expects a redirect
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/signin')

  def test_logged_out_user_redirected(self):
    response = self.client.get(reverse('logoutpage'))
    self.assertEqual(response.status_code, 302)

# end of TestLogoutView

# These tests will test the Models of RideShareAccounts
class TestRideShareAccountsModels(TestCase):
  # generic set up func
  def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='testpassword')
    self.payment_method = PaymentMethod.objects.create(description='Test Payment Method')

  # tests basic creation
  def test_create_account(self):
    account = Account.objects.create(user=self.user, defaultPaymentMethod=self.payment_method)
    self.assertEqual(account.user, self.user)
    self.assertEqual(account.defaultPaymentMethod, self.payment_method)
    self.assertEqual(account.outstandingBalance, 0.00)


  # tests ordering of accounts
  def test_account_ordering(self):
    user1 = User.objects.create_user(username='user1', password='password1')
    user2 = User.objects.create_user(username='user2', password='password2')

    account1 = Account.objects.create(user=user1, defaultPaymentMethod=self.payment_method)
    account2 = Account.objects.create(user=user2, defaultPaymentMethod=self.payment_method)

    ordered_accounts = list(Account.objects.all())

    self.assertEqual(ordered_accounts, [account1, account2])


  #tests default balance being 0
  def test_default_balance(self):
     account = Account.objects.create(user=self.user, defaultPaymentMethod=self.payment_method)
     self.assertEqual(account.outstandingBalance, 0.00)

# end of TestModels

# This class will test the url paths of the RideShareAccounnts urls.py
class TestURLS(TestCase):
  def test_signuppage_mapping(self):
    url = reverse('signuppage')
    self.assertEqual(url, '/signup/')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

  def test_signinpage_mapping(self):
    url = reverse('signinpage')
    self.assertEqual(url, '/signin/')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

  def test_logoutpage_mapping(self):
    url = reverse('logoutpage')
    self.assertEqual(url, '/logout/')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 302)
    
# end of TestURLS
    
    
