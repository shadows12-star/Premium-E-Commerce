from django.contrib import messages
from orders.models import Order, OrderProduct
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account, UserProfile
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .utils import send_password_reset_email, send_verification_email
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from cart.models import Cart, CartItem
from cart.views import create_cart_id
from .forms import UserProfileForm
# Create your views here.
def login(request):
    next_url=request.GET.get('next')or request.POST.get('next')
    if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email,password)
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                try:                    
                    cart = Cart.objects.get(cart_id=create_cart_id(request))
                    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
                    if cart_items.exists():
                         for item in cart_items:
                            item.user = user
                            item.cart = None
                            item.save()
                    
                except Cart.DoesNotExist:
                    pass
                auth_login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect(next_url) if next_url else redirect('profile')
            else:
               messages.error(request, 'Invalid email or password.')
               return redirect('login')
                
            
    return render(request, 'accounts/login.html')
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(
                email=email,
                username=email.split('@')[0],
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            user.phone_number = phone_number
            user.save()
            send_verification_email(request, user)
            messages.success(request, 'Please check your email to verify your account before logging in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    context={
        'form':form
    }
    return render(request, 'accounts/register.html',context)
@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        messages.success(request, "Your account has been verified. You can now log in.")
        return redirect("login")

    messages.error(request, "Verification link is invalid or expired.")
    return redirect("register")
@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    
    order_products = OrderProduct.objects.filter(order__in=orders)
    total_price=0
    for order_product in order_products:
        total_price+=order_product.product.price*order_product.quantity


    return render(request, 'accounts/profile.html', {
        'orders': orders,
        'order_products': order_products,
        'total_price': total_price,
        'order_count': order_products.count(),

    })

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Account.objects.get(email__iexact=email)
            send_password_reset_email(request, user)
            messages.success(request, 'A password reset link has been sent to your email.')
            return redirect('login')
        except Account.DoesNotExist:
            messages.error(request, 'No account found with that email address.')
            return redirect('forgot_password')
        
    return render(request, 'accounts/forgot_password.html')
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            if new_password != confirm_new_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('password_reset_confirm', uidb64=uidb64, token=token)


            user.set_password(new_password)
            user.save() 
            messages.success(request, 'Your password has been reset successfully. You can now log in.')
            return redirect('login')
        return render(request, 'accounts/password_reset_confirm.html')
    else:
        messages.error(request, 'Password reset link is invalid or expired.')
        return redirect('forgot_password')
def User_profile(request):
    
    
    if request.method == 'POST':
       try:
            profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated.')
                return redirect('edit_profile')
       except UserProfile.DoesNotExist:
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                new_profile = form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
                messages.success(request, 'Your profile has been created.')
                return redirect('edit_profile')
    else:
        try:
            profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(instance=profile)
        except UserProfile.DoesNotExist:
            form = UserProfileForm()
   
    return render(request, 'accounts/edit_profile.html', {'form': form})
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, 'Your current password is incorrect.')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('change_password')


        user.set_password(new_password)
        user.save()

       
        update_session_auth_hash(request, user)

        messages.success(request, 'Your password has been changed successfully.')
        return redirect('profile')

    return render(request, 'accounts/change_password.html')
def Order_details(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order_products = OrderProduct.objects.filter(order=order)
    total_price=0
    for order_product in order_products:
        total_price+=order_product.product.price*order_product.quantity
    context={
        'order':order,
        'order_products':order_products,
        'total_price':total_price,
    }
    return render(request, 'accounts/order_details.html', context)