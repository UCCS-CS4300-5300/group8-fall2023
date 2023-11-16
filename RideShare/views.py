from django.shortcuts import render, redirect

def home(request):
  if not request.user.is_authenticated:
    return redirect('/signin')
    
  return render(request, 'home.html')

def checkoutSuccess(request):
  return render(request, 'checkoutSuccess.html')

def checkinSuccess(request):
  return render(request, 'checkinSuccess.html')