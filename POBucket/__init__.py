from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import os
import pymysql


pymysql.install_as_MySQLdb()


def send_mail(html_content, user, subject: str):
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=os.environ.get("EMAIL_HOST_USER"),
        to=[user.email]
    ); msg.attach_alternative(html_content, "text/html")
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
