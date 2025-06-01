from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
from django.contrib import messages

from seller.models import Product, Bid
from .models import Buyer, RouteError

from . import login_required
# from . import razorpay_client

from termcolor import cprint
from sqlite3 import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


# index route (default)
def index(request):
    return render(request, "index.html", {"title": "Home"})


# login route
def login(request):
    if request.method == "GET":
        return render(request, "loginAndRegister.html", {"title": "Buyer-Login"})

    if request.method == "POST":
        if (request.POST.get("email") in request.session) and (request.session[request.POST.get("email")] == True):
            return redirect("buyer-portal", buyer=request.POST.get("email"))

        else:
            try:
                buyer = Buyer.objects.get(email=request.POST.get("email"))
                cprint(f"User -> {buyer}", "yellow"); cprint(f"User Email -> {buyer.email}", "light_cyan")
            except Buyer.DoesNotExist:
                return render(
                    request,
                    "loginAndRegister.html",
                    {
                        "loginErrorMsg": "Invalid email!!".upper(),
                    },
                )
            try:
                if check_password_hash(buyer.password, password=request.POST.get("password")):
                    request.session[buyer.email] = True
                    cprint(f"{buyer.email} authenticated successfully!!".upper(), "green", attrs=["bold"],)
                    return redirect("buyer-portal", buyer=buyer.email)

                else:
                    return render(
                        request,
                        "loginAndRegister.html",
                        {
                            "title": "Buyer-Login",
                            "loginErrorMsg": "Invalid emai or password!!".upper(),
                        },
                    )

            except Exception as E:
                error = RouteError(
                    title="Buyer Authentication", message=E, field="Login Route"
                )
                error.save()

                return render(
                    request,
                    "loginAndRegister.html",
                    {
                        "title": "Buyer-Login",
                        "loginErrorMsg": "Unable to authenticate you!!".upper(),
                    },
                )


# logout route
def logout(request, buyer):
    if request.session:
        request.session.pop(buyer, None)
    return redirect("buyer-login")


# register route
def register(request):
    if request.method == "GET":
        return render(request, "loginAndRegister.html", {"title": "Buyer-SignUp"})

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        cprint(f"Entered Data: {username, email, password}", "green")

        if Buyer.objects.filter(email=email).exists():
            return render(
                request,
                "loginAndRegister.html",
                {
                    "title": "Buyer-SignUp",
                    "signUpErrorMsg": "Email already exists!!".upper(),
                },
            )

        elif password == confirm_password:
            cprint(f"Email: {email} is good to go!", "green", attrs=["bold"])
            try:
                buyer = Buyer(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                )
                buyer.save()

                return redirect("buyer-login")

            except IntegrityError as IE:
                error = RouteError(
                    title="Buyer Registration", message=IE, field="Registration Route"
                )
                error.save()

                return redirect("admin")


# portal route
@login_required
def portal(request, buyer):
    if request.method == "GET":
        products = Product.objects.all()
        buyer = get_object_or_404(Buyer, email=buyer)
        return render(request, "portal.html",
            {
                "title": "Buyer Portal",
                "products": products,
                "buyer": buyer,
            },
        )


# TODO
# profile route
@login_required
def profile(request, buyer):
    user = Buyer.objects.get(email=buyer)
    user_data = request.POST.dict()

    try:
        if "updatedUsername" in user_data:
            usernames = list(Buyer.objects.values_list("username", flat=True))
            if user_data["updatedUsername"] in usernames:
                messages.error(request, "Username already exist")
                return redirect("buyer-portal", buyer=buyer)

            else: user.username = user_data["updatedUsername"]

        if "updatedEmail" in user_data:
            user.email = user_data["updatedEmail"]; user.save()
            messages.info(request, "Email updated successfully. Re-Login required")
            return redirect('buyer-logout', buyer=buyer)

        if "updatedPhoneNo" in user_data: user.phone = user_data["updatedPhoneNo"]

    except Exception as E:
        profileError = RouteError(
            title="Profile update issue",
            field="Profile Route",
            message=E,
        ); profileError.save()

        messages.error(request, f"Unable to update data. Reason: {E}")
        return redirect('buyer-portal', buyer=buyer)

    finally: user.save()

    messages.success(request, "Data updated successfully!")
    return redirect("buyer-portal", buyer=buyer)


# history route
@login_required
def history(request, buyer):
    return render(request, "history.html",
        {
            "title": "history",
            "buyer": buyer
        }
    )


# bid route
@login_required
def place_bid(request, buyer, pid):
    product = get_object_or_404(Product, pid=pid)
    buyer = get_object_or_404(Buyer, email=buyer)

    if request.method == "POST":
        bid_amount = request.POST.get("bid-amount")
        bid_amount = float(bid_amount)

        # Create and save bid
        bid = Bid.objects.create(product=product, bidder=buyer, bid_amount=bid_amount)
        bid.save()

        # updating product price
        product.price = bid_amount
        product.save()

        messages.success(
            request, f"Bid of ₹{bid_amount} placed successfully on {product.name}."
        )
        return redirect("buyer-portal", buyer=buyer.email)

    return redirect("buyer-portal", buyer=buyer.username)
