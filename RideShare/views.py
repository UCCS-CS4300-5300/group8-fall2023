from django.shortcuts import render, redirect

def home(request):
  if not request.user.is_authenticated:
    return redirect('/signin')
    
  return render(request, 'home.html')

