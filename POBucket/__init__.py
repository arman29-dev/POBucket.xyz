from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from secrets import choice

import os
import pymysql


pymysql.install_as_MySQLdb()


def get_uid(user):
    while True:
        uid = ''.join(choice('0123456789') for _ in range(10))
        if user.objects.filter(uid=uid).exists(): continue
        else: return uid


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


def send_mail(html_content, user, subject: str, file: str|None=None):
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=os.environ.get("EMAIL_HOST_USER"),
        to=[user.email]
    )

    msg.attach_alternative(html_content, "text/html")

    if (file is not None) and (os.path.exists(file)):
        msg.attach_file(file)

    msg.send()

def send_wlcm_email(user):
    html_content = render_to_string("emails/welcome.html", {'username': user.username, 'email': user.email, 'id': user.uid})
    send_mail(html_content, user, "Welcome to P.O.B")

def send_acnt_verify_mail(user, code: str):
    html_content = render_to_string("emails/accountVerificationCode.html", {'code': code})
    send_mail(html_content, user, "P.O.B Account Verification Code")

def send_prc_email(user, code: str):
    html_content = render_to_string("emails/passwordResetCode.html", {'code': code})
    send_mail(html_content, user, "P.O.B Password Reset Code")

def send_2FA_BC_email(user, file: str):
    html_content = render_to_string("emails/sellerWelcomeW2FA.html",
        {
            'email': user.email,
            'uid': user.uid,
        }
    ); send_mail(html_content, user, "P.O.B 2FA Code", file=file)
