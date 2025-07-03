from django.shortcuts import redirect

from functools import wraps

import secrets



def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        seller_email = kwargs.get('seller')

        is_authenticated = False
        if seller_email and request.session.get(seller_email) == True:
            is_authenticated = True

        if not is_authenticated:
            return redirect('seller-login')

        return view_func(request, *args, **kwargs)

    return wrapper


def get_uid(seller):
    while True:
        uid = ''.join(secrets.choice('0123456789') for _ in range(10))
        if seller.objects.filter(uid=uid).exists(): continue
        else: return uid


def create_pid(product, max_length: int=6):
    while True:
        pid = secrets.token_urlsafe(max_length)
        if product.objects.filter(pid=pid).exists(): continue
        else: return pid
