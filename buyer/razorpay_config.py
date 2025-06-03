from django.conf import settings
import razorpay
import dotenv
import os

dotenv.load_dotenv(f'{settings.BASE_DIR}/env/.env')

# Razorpay setup
RZP_TEST_ID = os.environ.get('RZP_TEST_ID')
RZP_TEST_SECRET = os.environ.get('RZP_TEST_SECRET')
razorpay_client = razorpay.Client(auth=(RZP_TEST_ID, RZP_TEST_SECRET))
razorpay_client.set_app_details({"title": "POBucket", "version": "1.0"})
