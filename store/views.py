from django.contrib import messages

from django.shortcuts import redirect, render

from cart.views import create_cart_id
from .models import Products,Variations,ProductReview
from cart.models import CartItem,Cart
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ProductReviewForm 
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
    form=ProductReviewForm()
    reviews=single_product.reviews.filter(product=single_product)
    context={
        'single_product':single_product,
        'colors':colors,
        'sizes':sizes,
        'form':form,
        'reviews':reviews,
        
    }
    
    
    return render(request, 'storetems/product_detail.html', context)
def submit_review(request, product_id):
    product = Products.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('product_details', category_slug=product.category.slug, product_slug=product.slug)
        else:
            messages.error(request, 'There was an error submitting your review. Please try again.')
    return redirect('product_details', category_slug=product.category.slug, product_slug=product.slug)