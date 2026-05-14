

from django.http import HttpResponse
from django.shortcuts import render
from store.models import Products,ProductReview
from cart.models import CartItem,Cart
from django.db.models import Q, Avg
from django.core.paginator import Paginator



def home(request):
    products=Products.objects.all().filter(is_available=True).annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'home.html', {'products': products})