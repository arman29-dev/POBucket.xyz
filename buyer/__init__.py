from functools import wraps
from django.conf import settings
from django.shortcuts import redirect

import razorpay
import dotenv
import os

dotenv.load_dotenv(f'{settings.BASE_DIR}/env/.env')

# Razorpay setup
RZP_TEST_ID = os.environ.get('RZP_TEST_ID')
RZP_TEST_SECRET = os.environ.get('RZP_TEST_SECRET')
razorpay_client = razorpay.Client(auth=(RZP_TEST_ID, RZP_TEST_SECRET))
razorpay_client.set_app_details({"title": "POBucket", "version": "1.0"})


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
