from functools import wraps
from django.conf import settings
from django.shortcuts import redirect

import dotenv


dotenv.load_dotenv(f'{settings.BASE_DIR}/env/.env')


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
