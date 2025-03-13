from django.contrib.auth.hashers import make_password as secure_password
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect, render
from django.contrib import messages

from seller.models import Product, Bid
from .models import Buyer, RouteError

from . import authenticate, login_required

from termcolor import cprint
from sqlite3 import IntegrityError
# from .forms import RegistrationForm


# index route (default)
def index(request):
    return render(request, 'index.html', 
                  {'title': 'Home'})


@login_required
def history(request):
    return render(request, 'history.html', 
                  {'title': 'history'})


# login route
def login(request):
    if request.method == 'GET':
        return render(request, 'loginAndRegister.html', 
                      {'title': 'Buyer-Login'}
                    )

    if request.method == 'POST':
        buyer = object()
        try: buyer = Buyer.objects.get(email=request.POST.get('email')); cprint(buyer.email, 'green')
        except Buyer.DoesNotExist:
            return render(request, 'loginAndRegister.html', 
                        {
                            'loginErrorMsg': "Invalid email!!".upper(),
                        }
                    )
        try:
            if authenticate(buyer, password=request.POST.get('password')):
                request.session['buyer'] = buyer.email
                cprint(f"{buyer.email} authenticated successfully!!".upper(), 
                       'green', attrs=['bold', 'blink'])
                return redirect('buyer-portal', buyer=buyer.email)

            else:
                return render(request, 'loginAndRegister.html', 
                                {
                                  'title': 'Buyer-Login',
                                  'loginErrorMsg': 'Invalid emai or password!!'.upper()
                                }
                            )

        except Exception as E:
            error = RouteError(
                title="Buyer Authentication",
                message=E,
                field='Login Route'
            ); error.save()

            return render(request, 'loginAndRegister.html', 
                            {
                              'title': 'Buyer-Login',
                              'loginErrorMsg': 'Unable to authenticate you!!'.upper()
                            }
                        )


# logout route
def logout(request):
    if request.session:
        request.session.flush()
    return redirect('buyer-login')


# register route
def register(request):
    if request.method == 'GET':
        return render(request, 'loginAndRegister.html', 
                      {'title': "Buyer-SignUp"}
                    )

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        cprint(f"Entered Data: {username, email, password}", 'green')

        if Buyer.objects.filter(email=email).exists():
            return render(request, 'loginAndRegister.html',
                          {
                            'title': 'Buyer-SignUp',
                            'signUpErrorMsg': 'Email already exists!!'.upper()
                          }
                        )

        elif password == confirm_password:
            cprint(f'Email: {email} is good to go!', 'green', attrs=['bold', 'blink'])
            try:
                buyer = Buyer(
                    username=username,
                    email=email,
                    password=secure_password(password),
                ); buyer.save()

                return redirect('buyer-login')

            except IntegrityError as IE:
                error = RouteError(
                    title="Buyer Registration",
                    message=IE,
                    field='Registration Route'
                ); error.save()

                return redirect('admin')


# portal route
@login_required
def portal(request, buyer):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'portal.html',
                      {
                        'title': 'Buyer Portal',
                        'products': products,
                        'buyer': buyer
                       }
                    )


# bid route
@login_required
def place_bid(request, buyer, pid):
    product = get_object_or_404(Product, pid=pid)
    buyer = get_object_or_404(Buyer, email=buyer)

    if request.method == 'POST':
        bid_amount = request.POST.get('bid-amount')
        bid_amount = float(bid_amount)

        # Create and save bid
        bid = Bid.objects.create(product=product, bidder=buyer, bid_amount=bid_amount)
        bid.save()

        messages.success(request, f"Bid of ₹{bid_amount} placed successfully on {product.name}.")
        return redirect('buyer-portal', buyer=buyer.email)

    return redirect('buyer-portal', buyer=buyer.username)