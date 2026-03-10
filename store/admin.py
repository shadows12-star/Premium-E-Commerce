from django.contrib import admin
from .models import Products
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available', 'created_date', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name',)
    list_display_links = ('product_name',)
    filter_horizontal = ()
    list_filter = ('is_available', 'created_date')
    fieldsets = ()
admin.site.register(Products, ProductAdmin)