from functools import wraps
from django.conf import settings
from django.shortcuts import redirect

import secrets
import dotenv


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
