from django.shortcuts import render

from cart.views import create_cart_id
from .models import Products,Variations
from cart.models import CartItem,Cart
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
def store(request,category_slug=None):
    products=Products.objects.all().filter(is_available=True)
    product_count=products.count()
   
    if category_slug:
        products=products.filter(category__slug=category_slug)
        product_count=products.count()
   
    search_query=request.GET.get('searchkeyword')
    if search_query:
         products=products.filter(Q(product_name__icontains=search_query)|Q(description__icontains=search_query)|Q(category__category_name__icontains=search_query)
                                  |Q(price__icontains=search_query))
         product_count=products.count()
    paginator=Paginator(products,3)
    page=request.GET.get('page')
    products=paginator.get_page(page)
    return render(request, 'storetems/store.html', {'products': products, 'product_count': product_count})


def product_details(request, category_slug,product_slug):
    try:
        single_product=Products.objects.get(category__slug=category_slug, slug=product_slug)
        
        
        
    except Exception as e:
        raise e
    variations=None
    if single_product.variations.exists():
        variations=single_product.variations.all()
        colors=variations.values_list('color', flat=True).distinct()
        sizes=variations.values_list('size', flat=True).distinct()
    else:
        colors=None
        sizes=None
    context={
        'single_product':single_product,
        'colors':colors,
        'sizes':sizes,
        
    }
    
    
    return render(request, 'storetems/product_detail.html', context)
    