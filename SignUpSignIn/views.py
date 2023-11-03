from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib import messages

def signuppage(request):
  if request.method == "POST":
    signup_form = SignUpForm(request.POST, request)
    if signup_form.is_valid():
      signup_form.save()
      messages.success(request, ('Sign up succeeded!'))
    else:
      messages.error(request, 'Sign up was unsuccessfull! Please try again.')


    return redirect("/signup")
  signup_form = SignUpForm()
  users = User.objects.all()
  return render(request=request, template_name="signup.html", context={'signup_form':signup_form, 'users':users})