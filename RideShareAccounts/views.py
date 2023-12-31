from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from RideShareAccounts.forms import SignUpForm, AccountForm, ChangePasswordForm
from RideShareAccounts.models import Account, PaymentMethod
from RideShareBilling.models import Payment


def signuppage(request):
    """
    This handles the sign up form.  It created a default user and relates it to the additional fields we need for an account.
    """

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

    form = SignUpForm()
    paymentMethods = PaymentMethod.objects.all()
    return render(request, 'signup.html', {'form': form, 'paymentMethods': paymentMethods})


def signinpage(request):
    """
    This is the view for the simple sign in page.
    """

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
    """
    This view just logs a user out and sends them to the sign in page.
    """

    logout(request)
    return redirect('/signin')


def accountpage(request):
    """
    This view has a lot going on.  It allows users to change account info, change password, pay a bill and see history.
    """

    if not request.user.is_authenticated:
        return redirect('/signin')

    if request.method == 'POST':
        form = AccountForm(request.POST)

        if form.is_valid():
            request.user.username = form.data['userName']
            request.user.email = form.data['userEmail']
            request.user.save()

            account = Account.objects.get(user=request.user)
            account.defaultPaymentMethod_id = form.data['defaultPaymentMethod']
            account.save()

    form = AccountForm()
    paymentMethods = PaymentMethod.objects.all()
    userPayments = Payment.objects.filter(user=request.user)
    account = Account.objects.get(user=request.user)
    return render(request, 'account.html',
                  {'form': form, 'user': request.user,
                   'defaultPaymentMethodId': account.defaultPaymentMethod_id,
                   'outstandingBalance': account.outstandingBalance,
                   'paymentMethods': paymentMethods, 'userPayments': userPayments})


def changepasswordpage(request):
    """
    This view allows a user to change their password.
    """

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('accountpage')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })
