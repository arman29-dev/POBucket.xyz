from django.shortcuts import render, redirect, HttpResponse

from .forms import RegistrationForm
from .models import Buyer, RouteError

from . import authenticate


# index route (default)
def index(request):
    return render(request, 'index.html', 
                  {'title': 'Home'})


# login route
def login(request):
    if request.method == 'GET':
        return render(request, 'loginAndRegister.html', 
                      {'title': 'Login'})

    if request.method == 'POST':
        buyer = Buyer.objects.get(email=request.POST.get('email'))
        try:
            if authenticate(buyer, password=request.POST.get('password')):
                request.session[buyer.email] = {
                    'id': buyer.id, 
                    'fullname': buyer.fullname, 
                    'phone': buyer.phone,
                }
                return redirect('buyer-portal')

            else:
                return render(request, 'loginAndRegister.html', 
                              {'message': 'Invalid emai or password!!'.upper(), 
                               'title': 'Login'})

        except Exception as E:
            error = RouteError(
                errorTitle="Buyer Authentication",
                errorMessage=E,
                errorField='Login Route'
            ); error.save()

            return render(request, 'loginAndRegister.html', 
                          {'message': 'Invalid emai or password!!'.upper(), 
                           'title': 'Login'})


# register route
def register(request):
    if request.method == 'GET':
        return render(request, 'loginAndRegister.html', 
                      {'title': 'Register'})

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('You are now registered')

        else:
            error = RouteError(
                errorTitle="Invalid Form",
                errorMessage=form.errors.as_text(),
                errorField='Register Route'
            ); error.save()

            return HttpResponse('Something went wrong')