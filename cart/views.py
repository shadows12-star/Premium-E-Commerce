from django.shortcuts import get_object_or_404, redirect, render
#import decimal
from decimal import Decimal

from numpy import size
# Create your views here.
from .models import Cart, CartItem
from store.models import Products,Variations

def create_cart_id(request):
    cart_id=request.session.session_key
    if not cart_id:
        request.session.create()
        cart_id=request.session.session_key
    return cart_id
def add_to_cart(request, product_id):
    product=Products.objects.get(id=product_id)
    size=None
    color=None
    variation=None
    if request.method == 'POST':
        size=request.POST['size']
        color=request.POST['color']
        variation=Variations.objects.filter(product=product, size=size, color=color, is_active=True).first()
       

  
    try:
        cart=Cart.objects.get(cart_id=create_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=create_cart_id(request))
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product, variation=variation, cart=cart)
        cart_item.quantity+=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(product=product, variation=variation, cart=cart, quantity=1)
        cart_item.save()



    return redirect('cart')
def cart(request):
   total=Decimal(0.00)
   tax=Decimal(0.00)
   try:
        cart=Cart.objects.get(cart_id=create_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
             total+=cart_item.sub_total()
        tax=total*Decimal(0.02)
       
       
   except Cart.DoesNotExist:
        cart_items=None
        
   context={
        'total': total,
        'cart_items': cart_items,
        'tax': tax,
   }

   return render(request, 'cart/cart.html', context)
def increase_to_cart(request, product_id,variation_id):
    cart=Cart.objects.get(cart_id=create_cart_id(request))
    product=get_object_or_404(Products, id=product_id)
    variation=get_object_or_404(Variations, id=variation_id)
    cart_item=CartItem.objects.get(product=product, variation=variation, cart=cart)
    cart_item.quantity+=1
    cart_item.save()
    return redirect('cart')
def remove_from_cart(request, product_id,variation_id):
    cart=Cart.objects.get(cart_id=create_cart_id(request))
    product=get_object_or_404(Products, id=product_id)
    variation=get_object_or_404(Variations, id=variation_id)
  
    cart_item=CartItem.objects.get(product=product, variation=variation, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
def delete_cart_item(request, product_id,variation_id):
    cart=Cart.objects.get(cart_id=create_cart_id(request))
    product=get_object_or_404(Products, id=product_id)
    variation=get_object_or_404(Variations, id=variation_id)
    cart_item=CartItem.objects.get(product=product, variation=variation, cart=cart)
    cart_item.delete()
    return redirect('cart')