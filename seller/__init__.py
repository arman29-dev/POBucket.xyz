from django.conf import settings
from django.shortcuts import redirect

from functools import wraps
from os.path import join

import secrets



def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        seller_email = kwargs.get('seller')

        is_authenticated = False
        if seller_email and request.session.get(f"seller-{seller_email}") == True:
            is_authenticated = True

        if not is_authenticated:
            return redirect('seller-login')

        return view_func(request, *args, **kwargs)

    return wrapper


def create_pid(product, max_length: int=6):
    while True:
        pid = secrets.token_urlsafe(max_length)
        if product.objects.filter(pid=pid).exists(): continue
        else: return pid


def generate_2FA_backup_codes(count: int=10, code_len: int=6):
    codes = list()
    for _ in range(count):
        code = ''.join(secrets.choice('0123456789') for _ in range(code_len))
        codes += [code]
    return codes


def write2FAcodes(seller_email: str, codes: list):
    filename = seller_email.split('@')[0]
    file = join(settings.BASE_DIR, 'Database', 'seller_2FA_BC', f'{filename}.txt')

    try:
        with open(file, 'w') as f:
            f.write("Your 2FA Backup Codes (keep them secret, each code is one-time-use)\n")
            f.write(f"There backup codes are for the `{seller_email}` account:\n\n")

            for i in range(0, len(codes), 2):
                left = codes[i]
                right = codes[i + 1] if i + 1 < len(codes) else ''
                f.write(f"{left:<15}\t{right}\n")

        return True
    except Exception as E:
        print(E); return False
