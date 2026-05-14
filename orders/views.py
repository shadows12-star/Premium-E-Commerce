import decimal

from django.urls import reverse
from store.models import Products, Variations
from django.shortcuts import redirect, render
from cart.models import CartItem
from .models import Order, OrderProduct, Payment
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from ecommerce.utils import generate_sslcommerz_payment_url, validate_sslcommerz_payment
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_order_confirmation_email
# Create your views here.
def place_order(request):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    grand_total=decimal.Decimal(0.00)
    tax=decimal.Decimal(0.00)
    for cart_item in cart_items:
        total=cart_item.product.price * cart_item.quantity
        grand_total+=total
        tax=grand_total * decimal.Decimal('0.18')
        grand_total+=tax
    if cart_count <= 0:
        return redirect('')
    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            order=form.save(commit=False)
            order.user=current_user
            order.order_total=grand_total
            order.tax=tax
            order.ip=request.META.get('REMOTE_ADDR')
            order.save()
            current_datetime=order.created_at.strftime('%Y%m%d%H%M%S')
            order.order_number=str(current_datetime)+str(order.id)

            order.save()
      
           
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payment.html', context)
    else:
        form=OrderForm()
    context={
        'form':form,
        'grand_total': grand_total,
        'tax': tax, 
        'cart_items': cart_items,
    }
    return render(request, 'orders/payment.html', context)


@csrf_exempt
def start_sslcommerz_payment(request, order_number):
    order = get_object_or_404(
        Order,
        user=request.user,
        order_number=order_number,
        is_ordered=False
    )

    try:
        response_data = generate_sslcommerz_payment_url(order, request)

        if response_data.get('status') == 'SUCCESS':
            gateway_url = response_data.get('GatewayPageURL')
            if gateway_url:
                return redirect(gateway_url)

        messages.error(request, 'Unable to initiate payment.')
        return redirect('checkout')

    except Exception as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('checkout')





@csrf_exempt
@transaction.atomic
def sslcommerz_success(request):
    val_id = request.POST.get('val_id') or request.GET.get('val_id')
    tran_id = request.POST.get('tran_id') or request.GET.get('tran_id')

    if not val_id or not tran_id:
        return HttpResponse("Invalid payment response", status=400)

    order = get_object_or_404(Order, order_number=tran_id)

    if order.is_ordered and order.payment:
        return render(request, 'orders/payment_success.html', {'order': order})

    validation_data = validate_sslcommerz_payment(val_id)

    if validation_data.get('status') not in ['VALID', 'VALIDATED']:
        return HttpResponse("Payment validation failed", status=400)

    if str(validation_data.get('tran_id')) != str(order.order_number):
        return HttpResponse("Transaction mismatch", status=400)

    payment = Payment.objects.create(
        user=order.user,
        payment_id=validation_data.get('val_id'),
        payment_method=validation_data.get('card_type', 'SSLCommerz'),
        amount_paid=validation_data.get('amount'),
        status=validation_data.get('status'),
    )

    order.payment = payment
    order.is_ordered = True
    order.status = 'Accepted'
    order.save()

    cart_items = CartItem.objects.filter(user=order.user)

    for cart_item in cart_items:
                order_product=OrderProduct()
                order_product.user=order.user
                order_product.order=order
                order_product.product=cart_item.product
                order_product.variations=cart_item.variation
                order_product.quantity=cart_item.quantity
                order_product.product_price=cart_item.product.price
                order_product.is_ordered = True
                order_product.payment = payment
                order_product.save()
                product = Products.objects.get(id=cart_item.product.id)
                product.stock -= cart_item.quantity
                product.save()
       
    
    cart_items.delete()
    #send order confirmation email here
    # send_order_confirmation_email(order)
    send_order_confirmation_email(order)
    

    return redirect(reverse('order_success', kwargs={'order_number': order.order_number}))
@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user, is_ordered=True)
    payment = order.payment
    return render(request, 'orders/payment_success.html', {
        'order': order,
        'payment': payment,
    }) 
# orders/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Order

@csrf_exempt
def sslcommerz_fail(request):
    tran_id = request.POST.get('tran_id') or request.GET.get('tran_id')

    if tran_id:
        try:
            order = Order.objects.get(order_number=tran_id, is_ordered=False)
            order.status = 'Cancelled'
            order.save()
        except Order.DoesNotExist:
            order = None
    else:
        order = None

    return render(request, 'orders/payment_fail.html', {
        'order': order,
    })
