from django.shortcuts import render
from .models import Products

# Create your views here.
def store(request,category_slug=None):
    products=Products.objects.all().filter(is_available=True)
    product_count=products.count()
    if category_slug:
        products=products.filter(category__slug=category_slug)
        product_count=products.count()
    return render(request, 'storetems/store.html', {'products': products, 'product_count': product_count})


def product_details(request, category_slug,product_slug):
    try:
        single_product=Products.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'storetems/product_detail.html', {'single_product': single_product})
    