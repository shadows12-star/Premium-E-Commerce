from cart.models import CartItem, Cart
from cart.views import create_cart_id


def total_items(request):
    if 'admin' in request.path:
        return {}

    total = 0

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=create_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.quantity

    except Cart.DoesNotExist:
        total = 0

    return {'total_items': total}