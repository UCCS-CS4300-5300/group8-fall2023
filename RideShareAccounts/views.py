from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from RideShareAccounts.forms import SignUpForm, AccountForm
from RideShareAccounts.models import Account, PaymentMethod


def signuppage(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            account = Account(user_id=user.id, defaultPaymentMethod_id=(request.POST['defaultPaymentMethod']))
            account.save()

            login(request, user)
            return redirect('/')

        else:
            paymentMethods = PaymentMethod.objects.all()
            return render(request, 'signup.html', {'form': form, 'paymentMethods': paymentMethods})

    else:
        form = SignUpForm()
        paymentMethods = PaymentMethod.objects.all()
        return render(request, 'signup.html', {'form': form, 'paymentMethods': paymentMethods})


def signinpage(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm()
            return render(request, 'signin.html', {'form': form})

    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})


def logoutpage(request):
    logout(request)
    return redirect('/signin')


def accountpage(request):
    if not request.user.is_authenticated:
        return redirect('/signin')

    if request.method == 'POST':
        form = AccountForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            account = Account(user_id=user.id, defaultPaymentMethod_id=(request.POST['defaultPaymentMethod']))
            account.save()

            login(request, user)
            return redirect('/')

        else:
            paymentMethods = PaymentMethod.objects.all()
            return render(request, 'account.html', {'form': form, 'paymentMethods': paymentMethods})

    else:
        form = AccountForm()
        paymentMethods = PaymentMethod.objects.all()
        return render(request, 'account.html', {'form': form, 'paymentMethods': paymentMethods})
