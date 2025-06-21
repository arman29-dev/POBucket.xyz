from django.utils import timezone
from django.shortcuts import get_object_or_404

from seller.models import Sale
from .models import Payment, RouteError

from nanoid import generate


def process_successful_payment(payment_id):
    """
    Process a successful payment by creating a Sales record.

    Args:
        payment_id (str): The Razorpay payment ID

    Returns:
        Sales: The created Sales record if successful, None otherwise
    """
    try:
        # Get the payment record
        payment = get_object_or_404(Payment, payment_id=payment_id)

        # Check if payment status is successful
        if payment.status == "completed":
            # Get related data
            product = payment.product
            buyer = payment.buyer
            seller = product.seller

            # Create a new sales record
            sale = Sale(
                product=product,
                seller=seller,
                buyer=buyer,
                payment=payment,
                final_price=payment.amount,  # Use the amount from payment
                sale_date=timezone.now()
            ); sale.save()

            # Update product status - mark as sold
            if product.bid_status:
                product.bid_status = False  # Close bidding if it was an auction
                product.save()

            # Log the successful sale
            print(f"Sale recorded: {product.name} sold to {buyer.fullname} for ₹{payment.amount}")
            return sale

        else:
            print(f"Payment {payment_id} status is {payment.status}, not creating sale record")
            return None

    except Exception as E:
        # Log the error
        error = RouteError(
            eid = generate(size=10),
            title="Sales Record Creation Error",
            field="Payment Processing",
            message=str(E)
        ); error.save()

        print(f"Error creating sales record: {str(E)}")
        return E


def update_payment_and_create_sale(order_id, payment_id, status="completed"):
    """
    Update a payment status and create a sales record if successful.

    Args:
        order_id (str): The Razorpay order ID
        payment_id (str): The Razorpay payment ID
        status (str): The payment status (default: "completed")

    Returns:
        tuple: (Payment object, Sales object or None)
    """
    try:
        # Get the payment record
        payment = get_object_or_404(Payment, order_id=order_id)

        # Update payment details
        payment.payment_id = payment_id
        payment.status = status
        payment.save()

        # If payment is successful, create a sales record
        if status == "completed":
            sale = process_successful_payment(payment_id)
            return payment, sale

        return payment, None

    except Exception as e:
        # Log the error
        error = RouteError(
            eid = generate(size=10),
            title="Payment Update Error",
            field="Payment Processing",
            message=str(e)
        )
        error.save()
        print(f"Error updating payment: {str(e)}")
        return None, None
