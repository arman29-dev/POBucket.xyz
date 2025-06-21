from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

from seller.models import Product, Bid
from .models import Buyer, Payment, RouteError

from .payment_utils import process_successful_payment
from . import login_required, send_prc_email, hide_email
from .razorpay_config import create_rzp_client, RZP_TEST_ID

from termcolor import cprint
from nanoid import generate
from sqlite3 import IntegrityError
from razorpay.errors import SignatureVerificationError
from werkzeug.security import generate_password_hash, check_password_hash

import json


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
                    eid=generate(size=10),
                    title="Buyer Authentication",
                    message=E,
                    field="Login Route"
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
                    eid=generate(size=10),
                    title="Buyer Registration",
                    message=IE,
                    field="Registration Route"
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
            eid=generate(size=10),
            title="Profile update issue",
            field="Profile Route",
            message=E,
        ); profileError.save()

        messages.error(request, f"Unable to update data. Reason: {E}")
        return redirect('buyer-portal', buyer=buyer)

    finally: user.save()

    messages.success(request, "Data updated successfully!")
    return redirect("buyer-portal", buyer=buyer)


# password reset route
@login_required
@csrf_protect
def password_reset(request, buyer):
    user = get_object_or_404(Buyer, email=buyer)
    hidden_email = hide_email(user.email)

    if request.method == "GET":
        code = user.generate_2FA_code()
        try:
            send_prc_email(user, code)
            messages.success(request, f"Email with 2FA code sent to {hidden_email} for resetting the password!")

        except Exception as E:
            error = RouteError(
                eid=generate(size=10),
                title="Issue mailing 2FA code",
                field="Password Reset Route",
                message=E,
            ); error.save()

            messages.error(request, "Unable to email 2FA code")
            return redirect('buyer-portal', buyer=user)

        return render(request, 'passwordReset.html', {"buyer": user})

    if request.method == "POST":
        submitted_code = request.POST.get("2FA-code")
        is_valid, msg = user.validate_code(submitted_code)

        if is_valid:
            newPassword = request.POST.get("newPassword")
            newPassword = generate_password_hash(newPassword)

            try:
                user.password = newPassword; user.save()
                messages.success(request, msg + " new password updated successfully. Re-Login is required")
                return redirect('buyer-logout', buyer=user)

            except Exception as E:
                error = RouteError(
                    eid=generate(size=10),
                    title="issue in password update",
                    field="Password Reset Route",
                    message=E,
                ); error.save()

                messages.success(request, "Unable to update password")
                return redirect('buyer-password-reset', buyer=user)

        else:
            messages.error(request, msg)
            return render(request, 'passwordReset.html', {"buyer": user})


# TODO
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
        bid = Bid.objects.create(
            product=product,
            bidder=buyer,
            bid_amount=bid_amount
        ); bid.save()

        # updating product price
        product.price = bid_amount
        product.save()

        messages.success(
            request, f"Bid of ₹{bid_amount} placed successfully on {product.name}."
        )
        return redirect("buyer-portal", buyer=buyer.email)

    return redirect("buyer-portal", buyer=buyer.username)


# Payment Route
@login_required
def payment(request, buyer, pid):
    product = get_object_or_404(Product, pid=pid)
    user = get_object_or_404(Buyer, email=buyer)
    total_price = int(product.price) + 100

    if request.method == "GET":
        return render(
            request, 'rzpCheckout.html',
            {
                "user": user,
                "product": product,
                "total": total_price,
                "razorpay_key": RZP_TEST_ID,
            },
        )

    if request.method == "POST":
        rzp_client = create_rzp_client()
        order = rzp_client.order.create(
            dict(
                amount=total_price*100,
                currency="INR",
                payment_capture="1",
                notes={
                    'buyer_id': str(buyer),
                    'product_id': str(pid),
                }
            )
        )

        # Store order details in session for verification later
        request.session[f'ODR-{order["id"]}'] = {
            'product_id': pid,
            'buyer_email': buyer,
            'amount': order["amount"],
            'status': 'created',
        }

        return JsonResponse({
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "razorpay_key": RZP_TEST_ID,
        })


# Payment verification route
@csrf_exempt
@require_POST
def verify_payment(request):
    try:
        # Get payment data from POST request
        payment_data = json.loads(request.body)
        razorpay_order_id = payment_data.get('razorpay_order_id')
        razorpay_payment_id = payment_data.get('razorpay_payment_id')
        razorpay_signature = payment_data.get('razorpay_signature')
        payment_method = payment_data.get('payment_method', 'Online Payment')
        product_name = payment_data.get('product_name')

        print(f"Payment verification for order: {razorpay_order_id}")
        print(f"Payment method: {payment_method}")

        # Verify the payment signature
        rzp_client = create_rzp_client()

        # Get order details from session
        order_data = request.session.get(f'ODR-{razorpay_order_id}')
        if not order_data:
            return render(
                request, 'paymentFailed.html',
                {
                    'error_message': "Order ID was not found of your payment process.",
                    'payment_id': razorpay_payment_id,
                    'product_name': product_name,
                    'amount': order_data['amount'] / 100,
                }
            )

        # Verify signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            rzp_client.utility.verify_payment_signature(params_dict)

            # Update order status in session
            order_data['status'] = 'success'
            order_data['payment_id'] = razorpay_payment_id
            request.session[f'ODR-{razorpay_order_id}'] = order_data

            # Create payment record in database
            buyer = get_object_or_404(Buyer, email=order_data['buyer_email'])
            product = get_object_or_404(Product, pid=order_data['product_id'])

            # Create Payment record
            payment = Payment(
                status='completed',
                buyer=buyer, product=product,
                order_id=razorpay_order_id,
                payment_id=razorpay_payment_id,
                amount=order_data['amount'] / 100,
                payment_method=payment_data.get('payment_method', 'Online Payment'),
            ); payment.save()

            # Create a sales record for the successful payment
            sale = process_successful_payment(razorpay_payment_id)

            # Store buyer email in session to maintain authentication after redirect
            request.session[order_data['buyer_email']] = True
            # Make sure session is saved immediately
            request.session.modified = True

            return render(
                request, 'paymentSuccess.html',
                {
                    'order_id': razorpay_order_id,
                    'product_name': product_name,
                    'amount': order_data['amount'] / 100,
                    'payment_method': payment_method,
                }
            )

        except SignatureVerificationError as SVE:
            # Update order status in session
            order_data['status'] = 'failed'
            request.session[f'ODR-{razorpay_order_id}'] = order_data

            return render(
                request, 'paymentFailed.html',
                {
                    'error_message': str(SVE),
                    'payment_id': razorpay_payment_id,
                    'product_name': product_name,
                    'amount': order_data['amount'] / 100,
                }
            )

    except Exception as E:
        eid = generate(size=10)
        error = RouteError(
            eid=eid,
            title="Payment Verification Error",
            field="Payment Verification Route",
            message=str(E)
        ); error.save()

        return render(
            request, '500.html',
            {
                'error_message': str(E),
                'eid': eid,
            }
        )
