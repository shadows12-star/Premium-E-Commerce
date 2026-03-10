from django.db import models
from django.urls import reverse
from categories.models import Category

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