from django.shortcuts import get_object_or_404, redirect, render
#import decimal
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from numpy import size
# Create your views here.
from .models import Cart, CartItem
from store.models import Products,Variations
from orders.forms import OrderForm

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
   
    if request.method == 'POST':
        size=request.POST['size']
        color=request.POST['color']
        variation=Variations.objects.filter(product=product, size=size, color=color, is_active=True).first()
        if variation is None:
            return redirect('cart')
       
    if request.user.is_authenticated:
         try:
            cart_item=CartItem.objects.get(product=product, variation=variation, user=request.user)
            cart_item.quantity+=1
            cart_item.save()
         except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(product=product, variation=variation, user=request.user, quantity=1)
            cart_item.save()
  
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
   if request.user.is_authenticated:
      try:
        cart_items=CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
             total+=cart_item.sub_total()
        tax=total*Decimal(0.02)
       
       
      except CartItem.DoesNotExist:
        cart_items=None
   else:
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
        'grand_total': total+tax,
   }

   return render(request, 'cart/cart.html', context)
def increase_to_cart(request, product_id,variation_id):
    if  request.user.is_authenticated:
         product=get_object_or_404(Products, id=product_id)
         variation=get_object_or_404(Variations, id=variation_id)
         cart_item=CartItem.objects.get(product=product, variation=variation, user=request.user)
         cart_item.quantity+=1
         cart_item.save()
    else:
       cart=Cart.objects.get(cart_id=create_cart_id(request))
       product=get_object_or_404(Products, id=product_id)
       variation=get_object_or_404(Variations, id=variation_id)
       cart_item=CartItem.objects.get(product=product, variation=variation, cart=cart)
       cart_item.quantity+=1
       cart_item.save()
    return redirect('cart')
def remove_from_cart(request, product_id,variation_id):
    if  request.user.is_authenticated:
         product=get_object_or_404(Products, id=product_id)
         variation=get_object_or_404(Variations, id=variation_id)
         cart_item=CartItem.objects.get(product=product, variation=variation, user=request.user)
         if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
         else:
            cart_item.delete()
    else:
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
    if request.user.is_authenticated:
         product=get_object_or_404(Products, id=product_id)
         variation=get_object_or_404(Variations, id=variation_id)
         cart_item=CartItem.objects.get(product=product, variation=variation, user=request.user)
         cart_item.delete()
    else:
      cart=Cart.objects.get(cart_id=create_cart_id(request))
      product=get_object_or_404(Products, id=product_id)
      variation=get_object_or_404(Variations, id=variation_id)
      cart_item=CartItem.objects.get(product=product, variation=variation, cart=cart)
      cart_item.delete()
    return redirect('cart')
@login_required
def checkout(request):
   total=Decimal(0.00)
   tax=Decimal(0.00)
   if request.user.is_authenticated:
      try:
        cart_items=CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
             total+=cart_item.sub_total()
        tax=total*Decimal(0.02)
       
       
      except CartItem.DoesNotExist:
        cart_items=None
   else:
     try:
         cart=Cart.objects.get(cart_id=create_cart_id(request))
         cart_items=CartItem.objects.filter(cart=cart, is_active=True)
         for cart_item in cart_items:
             total+=cart_item.sub_total()
             tax=total*Decimal(0.02)
       
       
     except Cart.DoesNotExist:
        cart_items=None
   form=OrderForm()
   context={
        'total': total,
        'cart_items': cart_items,
        'tax': tax,
        'form': form,
        'grand_total': total+tax,
   }
    
   return render(request, 'cart/checkout.html', context)