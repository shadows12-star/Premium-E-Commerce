from django.db import models
from django.urls import reverse
from categories.models import Category
from ecommerce import settings

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='photos/products', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
   

    def get_url(self):
        return reverse('product_details', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
size_choices=(
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', 'Double Extra Large'),
)
class Variations(models.Model):
    product=models.ForeignKey(Products, on_delete=models.CASCADE,related_name='variations')
    size=models.CharField(max_length=100, choices=size_choices, blank=True,null=True)
    color=models.CharField(max_length=100, blank=True,null=True)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name='variation'
        verbose_name_plural='variations'
        unique_together=(('product', 'size', 'color'),)
    def __str__(self):
        return self.size
rating_choices=(
    (1, '1 Star'),
    (2, '2 Stars'),
    (3, '3 Stars'),
    (4, '4 Stars'),
    (5, '5 Stars'),
)
class ProductReview(models.Model):
    product=models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review=models.TextField(max_length=500,blank=True,null=True)
    rating=models.IntegerField(choices=rating_choices)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.user.username} - {self.product.product_name}' 