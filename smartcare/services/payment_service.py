"""
Razorpay payment integration (test/sandbox mode). Isolates all Razorpay
SDK calls in one place so routes never touch the SDK directly.
"""

from decimal import Decimal

import razorpay
from flask import current_app


def _client():
    return razorpay.Client(
        auth=(current_app.config["RAZORPAY_KEY_ID"], current_app.config["RAZORPAY_KEY_SECRET"])
    )


def create_order(amount_rupees, receipt):
    """
    amount_rupees: rupee amount (e.g. 500 for ₹500)
    receipt: a short string identifying what this payment is for

    Returns the Razorpay order dict, which includes 'id' (order_id).
    Razorpay expects amount in the smallest currency unit (paise for INR).
    """
    amount_paise = int(Decimal(str(amount_rupees)) * 100)
    return _client().order.create(
        {
            "amount": amount_paise,
            "currency": current_app.config.get("RAZORPAY_CURRENCY", "INR"),
            "receipt": receipt,
            "payment_capture": 1,
        }
    )


def verify_payment_signature(order_id, payment_id, signature):
    """Returns True if the payment signature is authentic, False otherwise."""
    try:
        _client().utility.verify_payment_signature(
            {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
        )
        return True
    except razorpay.errors.SignatureVerificationError:
        return False