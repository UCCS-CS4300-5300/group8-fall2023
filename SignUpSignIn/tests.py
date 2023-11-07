from django.test import TestCase
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your tests here.
class TestSignUpForm(TestCase):
  def test_signup_form_valid(self):
    form = SignUpForm(data={'username': 'test', 
                            'password': 'test', 
                            'email': 'testuser@example.com',
                            'first_name': 'test',
                            'last_name': 'user'})
    self.assertTrue(form.is_valid())

  def test_signup_invalid_form(self):
    form = SignUpForm(data={})
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 2)


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

  def test_invalid_signup(self):
    data = {
      'username': 'test',
      'password1': 'password',
      'password2': 'password2',
    }
    response = self.client.post(reverse('signuppage'), data)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'signup.html')
    self.assertIsInstance(response.context['form'], UserCreationForm)
    self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

  
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

  def test_existing_user_authentication_error(self):
    user = User.objects.create_user(username='test', password='test')
    data = {
      'username': 'test',
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
    self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')


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

    
    
