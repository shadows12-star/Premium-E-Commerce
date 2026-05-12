# orders/utils.py
import requests
from django.conf import settings


def generate_sslcommerz_payment_url(order, request):
    post_data = {
        'store_id': settings.SSL_COMMERZ_STORE_ID,
        'store_passwd': settings.SSL_COMMERZ_STORE_PASSWORD,
        'total_amount': str(order.order_total),
        'currency': 'BDT',
        'tran_id': str(order.order_number),

        'success_url': request.build_absolute_uri('/orders/sslcommerz/success/'),
        'fail_url': request.build_absolute_uri('/orders/sslcommerz/fail/'),
        'cancel_url': request.build_absolute_uri('/orders/sslcommerz/cancel/'),
        'ipn_url': request.build_absolute_uri('/orders/sslcommerz/ipn/'),

        'cus_name': f"{order.first_name} {order.last_name}",
        'cus_email': order.email,
        'cus_add1': order.address_line_1,
        'cus_add2': order.address_line_2,
        'cus_city': order.city,
        'cus_state': order.state,
        'cus_country': order.country,
        'cus_phone': order.phone,

        'shipping_method': 'NO',
        'product_name': 'Order Payment',
        'product_category': 'Ecommerce',
        'product_profile': 'general',
    }

    response = requests.post(
        settings.SSL_COMMERTZ_PAYMENT_URL,
        data=post_data,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def validate_sslcommerz_payment(val_id):
    params = {
        'val_id': val_id,
        'store_id': settings.SSL_COMMERZ_STORE_ID,
        'store_passwd': settings.SSL_COMMERZ_STORE_PASSWORD,
        'format': 'json',
    }

    response = requests.get(
        settings.SSL_COMMERZ_VALIDATION_URL,
        params=params,
        timeout=30
    )
    response.raise_for_status()
    return response.json()