from django.contrib import messages

from django.shortcuts import redirect, render
from . models import ProductGallery, Products

from orders.models import Order, OrderProduct
from cart.views import create_cart_id
from .models import Products,Variations,ProductReview
from cart.models import CartItem,Cart
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ProductReviewForm 
from django.contrib.auth.decorators import login_required
from . models import Variations
#importing for average rating
from django.db.models import Avg
# Create your views here.
def store(request,category_slug=None):
    products=Products.objects.all().filter(is_available=True,stock__gt=0).order_by('created_date')
    
    min_price=request.GET.get('min_price','')
    max_price=request.GET.get('max_price','')
    available_variations=Variations.objects.filter(product__in=products, is_active=True).values('size').distinct()
    if request.GET.get('min_price') and request.GET.get('max_price'):
        min_price=request.GET.get('min_price')
        max_price=request.GET.get('max_price')
        products=products.filter(price__gte=min_price, price__lte=max_price)
        product_count=products.count()
    
   
    if category_slug:
        products=products.filter(category__slug=category_slug)
        product_count=products.count()
   
    search_query=request.GET.get('searchkeyword')
    if search_query:
         products=products.filter(Q(product_name__icontains=search_query)|Q(description__icontains=search_query)|Q(category__category_name__icontains=search_query)
                                  |Q(price__icontains=search_query))
         product_count=products.count()
    size=request.GET.get('size','')
    
    if size:
        variation_products=Variations.objects.filter(size=size, product__in=products).values_list('product_id', flat=True)
        products=products.filter(id__in=variation_products)
    product_count=products.count()
    paginator=Paginator(products,3)
    page=request.GET.get('page')
    products=paginator.get_page(page)
    return render(request, 'storetems/store.html', {'products': products, 'product_count': product_count, 'min_price': min_price, 
                                                    'max_price': max_price, 'available_variations': available_variations
                                                    })


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
    form=ProductReviewForm()
    reviews=single_product.reviews.filter(product=single_product)
    more_photos=single_product.gallery.all()
    avg_rating=reviews.aggregate(average_rating=Avg('rating'))['average_rating']
    context={
        'single_product':single_product,
        'colors':colors,
        'sizes':sizes,
        'form':form,
        'reviews':reviews,
        'avg_rating':avg_rating,
        'more_photos':more_photos,
        
    }
    
    
    return render(request, 'storetems/product_detail.html', context)

@login_required

def submit_review(request, product_id):
    product = Products.objects.get(id=product_id)
    order=OrderProduct.objects.filter(user=request.user, product=product,is_ordered=True).exists()
    if not order:
        messages.error(request, 'You need to purchase the product before submitting a review.')
        return redirect('product_details', category_slug=product.category.slug, product_slug=product.slug)
    if request.method == 'POST':
       if ProductReview.objects.filter(product=product, user=request.user).exists():
            review=ProductReview.objects.get(product=product, user=request.user)
            form = ProductReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your review has been updated.')
                return redirect('product_details', category_slug=product.category.slug, product_slug=product.slug)
       else:
            form = ProductReviewForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.product = product
                new_review.user = request.user
                new_review.save()
                messages.success(request, 'Your review has been submitted.')
                return redirect('product_details', category_slug=product.category.slug, product_slug=product.slug)
    return redirect('product_details', category_slug=product.category.slug, product_slug=product.slug)