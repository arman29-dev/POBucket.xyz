from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

from .models import Seller, RouteError
from . import get_uid, login_required

from nanoid import generate
from os.path import join
from qrcode import make
from pyotp import TOTP
from json import loads



def login(req):
    if req.method == "GET":
        return render(req, 'seller/loginAndRegister.html')

    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')

        try:
            seller = get_object_or_404(Seller, email=email)
            if check_password(password, seller.password):
                req.session[seller.email] = True
                return redirect('seller-dashboard', seller=seller.email)

            else:
                messages.error(req, 'Invalid password!')
                return render(req, 'seller/loginAndRegister.html')

        except Exception:
            messages.error(req, 'Invalid email!')
            return render(req, 'seller/loginAndRegister.html')


def register(req):
    if req.method == "GET":
        return render(req, 'seller/loginAndRegister.html')

    if req.method == "POST":
        seller_data = req.POST.dict()

        if Seller.objects.filter(email=seller_data['email']).exists():
            messages.warning(req, 'Username already exist! Take something else.')
            return render(req, 'seller/loginAndRegister.html')

        try:
            seller = Seller(
                uid=get_uid(Seller),
                username=seller_data['username'],email=seller_data['email'],
                password=make_password(seller_data['password'])
            ); seller.save()

            return redirect('seller-2FA-setup', uid=seller.uid)

        except Exception as E:
            print(f"Error registering seller: {E}")
            error = RouteError(
                eid=generate(size=10),
                title="Seller Registration",
                route="Register Route",
                message=E,
            ); error.save()

            messages.error(req, 'An error occurred while registering.')
            return render(req, 'seller/loginAndRegister.html')


def TwoFA(req, uid):
    if req.method == "GET":
        seller = get_object_or_404(Seller, uid=uid)
        seller.generate_2fa_secret()

        otp_uri = seller.get_otp_uri()
        img = make(otp_uri)

        qr_file_path = join(settings.MEDIA_ROOT, 'auth-QRs', f'{seller.uid}.png')
        seller.qr_code_path = f"auth-QRs/{seller.uid}.png"; seller.save()
        img.save(qr_file_path)

        return render(req, 'seller/2FA-setup.html',
            {
                'seller': seller,
            }
        )

    if req.method == "POST":
        data = loads(req.body)
        code = data.get('verification_code')
        seller_email = data.get('seller_email')

        seller = get_object_or_404(Seller, email=seller_email)
        totp = TOTP(seller.twoFA_secret)
        if totp.verify(code):
            req.session[seller.email] = True

            return JsonResponse({
                'success': True,
                'message': '2FA enabled successfully',
            })

        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid verification code'
            }, status=400)


def logout(req, seller):
    if req.session:
        req.session.pop(seller, None)
    return redirect("seller-login")


@login_required
def dashboard(req, seller):
    if req.method == "GET":
        return HttpResponse(b"Hello Welcome to the seller dashboard!")
