from functools import wraps
from django.conf import settings
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

import secrets
import dotenv
import os

dotenv.load_dotenv(f'{settings.BASE_DIR}/env/.env')


def get_uid(buyer):
    while True:
        uid = ''.join(secrets.choice('0123456789') for _ in range(10))
        if buyer.objects.filter(uid=uid).exists(): continue
        else: return uid


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        buyer_email = kwargs.get('buyer')

        is_authenticated = False
        if buyer_email and request.session.get(buyer_email) == True:
            is_authenticated = True

        if not is_authenticated:
            return redirect('buyer-login')

        return view_func(request, *args, **kwargs)

    return wrapper


def hide_email(email: str) -> str:
    try:
        local_part, domain = email.split("@")

        if len(local_part) <= 7:
            visible_start = local_part[:1]
            visible_end = local_part[-1:]
            return f"{visible_start}***{visible_end}@{domain}"

        visible_start = local_part[:4]
        visible_end = local_part[-3:]
        masked = '*' * (len(local_part) - len(visible_start) - len(visible_end))
        return f"{visible_start}{masked}{visible_end}@{domain}"

    except ValueError:
        raise ValueError("Invalid email format")


def send_mail(html_content, user, subject: str):
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=os.environ.get("EMAIL_HOST_USER"),
        to=[user.email]
    ); msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_wlcm_email(user):
    html_content = render_to_string("emails/welcome.html", {'username': user.username, 'email': user.email, 'id': user.id})
    send_mail(html_content, user, "Welcome to P.O.B")

def send_acnt_verify_mail(user, code: str):
    html_content = render_to_string("emails/accountVerificationCode.html", {'code': code})
    send_mail(html_content, user, "P.O.B Account Verification Code")

def send_prc_email(user, code: str):
    html_content = render_to_string("emails/passwordResetCode.html", {'code': code})
    send_mail(html_content, user, "P.O.B Password Reset Code")
