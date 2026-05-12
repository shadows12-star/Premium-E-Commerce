from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import OrderProduct

def send_order_confirmation_email(order):
    subject = f'Order Confirmation - Your Order #{order.order_number}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [order.email]

    ordered_products = OrderProduct.objects.filter(order=order).select_related('product', 'variations')

    context = {
        'order': order,
        'user': order.user,
        'ordered_products': ordered_products,
    }

    html_content = render_to_string('orders/order_confirmation_email.html', context)

    email = EmailMultiAlternatives(
        subject=subject,
        body='YOUR ORDER HAS BEEN PLACED SUCCESSFULLY.',
        from_email=from_email,
        to=to_email,
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)