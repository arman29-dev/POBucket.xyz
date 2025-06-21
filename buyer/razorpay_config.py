import os
import dotenv
import razorpay

from django.conf import settings

dotenv.load_dotenv(f'{settings.BASE_DIR}/env/.env')

# Razorpay setup
RZP_TEST_ID = os.environ.get('RZP_TEST_ID')
RZP_TEST_SECRET = os.environ.get('RZP_TEST_SECRET')
RZP_WEBHOOK_SECRET = os.environ.get("RZP_WEBHOOK_SECRET")

def create_rzp_client():
    rzp_client = razorpay.Client(auth=(RZP_TEST_ID, RZP_TEST_SECRET))
    rzp_client.set_app_details({"title": "POBucket", "version": "1.0"})

    return rzp_client
