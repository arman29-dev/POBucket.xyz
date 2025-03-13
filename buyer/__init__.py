from functools import wraps
from django.db.models import Model
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password


# function to authenticate user
def authenticate(model=Model, **credentials) -> bool:
    if check_password(credentials.get('password'), model.password):
        return True
    else: return False



def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        buyer_email = kwargs.get('buyer')

        is_authenticated = False
        if buyer_email and request.session.get('buyer') == buyer_email:
            is_authenticated = True

        if not is_authenticated:
            return redirect('buyer-login')

        return view_func(request, *args, **kwargs)

    return wrapper