from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

from POBucket import get_uid, hide_email, send_acnt_verify_mail, send_2FA_BC_email
from . import login_required, generate_2FA_backup_codes, write2FAcodes
from .models import Seller, BackupCodes, RouteError

from nanoid import generate
from os.path import join
from qrcode import make
from pyotp import TOTP
from json import loads



# Login Route
def login(req):
    if req.method == "GET":
        return render(req, 'seller/loginAndRegister.html')

    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')
        twoFAorBackupCode = req.POST.get('2faOrBC')

        try:
            seller = get_object_or_404(Seller, email=email)

            if seller.verify2FAcode(twoFAorBackupCode):
                if check_password(password, seller.password):
                    if seller.is_verified:
                        req.session[f"seller-{seller.email}"] = True
                        return redirect('seller-dashboard', seller=seller.email)

                    else:
                        messages.error(req, 'Account not verified.')
                        return render(req, 'seller/loginAndRegister.html')

                else:
                    messages.error(req, 'Invalid password!')
                    return render(req, 'seller/loginAndRegister.html')

            else:
                messages.error(req, 'Invalid 2FA/Backup code!')
                return render(req, 'seller/loginAndRegister.html')

        except Exception:
            messages.error(req, "User doesn't exist!")
            return render(req, 'seller/loginAndRegister.html')


# Registration Route
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

            return redirect('seller-email-verification', id=seller.uid)

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


# Email Verification Route
@csrf_exempt
def verify_email(req, id):
    if req.method == "GET":
        seller = get_object_or_404(Seller, uid=id)
        code = seller.generate_verification_code()

        send_acnt_verify_mail(seller, code)

        messages.info(req, f'Check {hide_email(seller.email)} for account verification code')
        return render(req, 'accountVerification.html',
            {
                "user": seller,
                'apiUrl': reverse('seller-email-verification',
                    kwargs={
                        'id': seller.uid
                    }
                )
            }
        )

    if req.method == "POST":
        data = loads(req.body)
        code = data.get('code')
        uid = data.get('uid')

        seller = get_object_or_404(Seller, uid=uid)
        is_valid, msg = seller.validate_code(code)

        if is_valid:
            seller.is_verified = True
            seller.clear_verification_code()
            seller.save()

            return JsonResponse(
                {
                    'success': True,
                    'message': 'Email verification successfully.',
                    'redirectUrl': reverse('seller-2FA-setup', kwargs={'uid': seller.uid})
                }
            )

        else:
            return JsonResponse(
                {
                    'success': False,
                    'message': msg,
                }, status=401
            )


# 2FA setup Route
def setup2FA(req, uid):
    if req.method == "GET":
        seller = get_object_or_404(Seller, uid=uid)
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
            req.session[f"seller-{seller.email}"] = True

            try:
                backup_2FA_codes = generate_2FA_backup_codes()
                user_backup_codes = BackupCodes(
                    seller=seller,
                    codes=backup_2FA_codes
                ); user_backup_codes.save()

                if write2FAcodes(seller.email, backup_2FA_codes):
                    file = join(settings.BASE_DIR, 'Database', 'seller_2FA_BC', f"{seller.email.split('@')[0]}.txt")
                    send_2FA_BC_email(seller, file)

            except Exception as E:
                error = RouteError(
                    eid=generate(size=10),
                    title="Emailing 2FA-BC",
                    route="setup2FA Route",
                    message=str(E)
                ); error.save()

            finally:
                return JsonResponse({
                    'success': True,
                    'message': '2FA enabled successfully',
                })

        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid verification code'
            }, status=400)


# Logout Route
def logout(req, seller):
    if req.session:
        req.session.pop(f"seller-{seller}", None)

    messages.warning(req, 'You have been logged out.')
    return redirect("seller-login")


# Dashboard Route
@login_required
def dashboard(req, seller):
    if req.method == "GET":
        return HttpResponse(b"Hello Welcome to the seller dashboard!")
