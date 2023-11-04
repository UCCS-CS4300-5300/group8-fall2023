from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def signuppage(request):

      if request.user.is_authenticated:
          return redirect('/')

      if request.method == 'POST':
          form = UserCreationForm(request.POST)

          if form.is_valid():
              form.save()
              username = form.cleaned_data['username']
              password = form.cleaned_data['password1']
              user = authenticate(username = username,password = password)
              login(request, user)
              return redirect('/')

          else:
              return render(request,'signup.html',{'form':form})

      else:
          form = UserCreationForm()
          users = User.objects.all()
          return render(request,'signup.html',{'form':form, 'users':users})