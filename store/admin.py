from django.contrib import admin
from .models import ProductReview, Products,Variations
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
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'is_active', 'created_date')
    list_filter = ('is_active', 'created_date')
    search_fields = ('product__product_name',)
admin.site.register(Variations, VariationAdmin)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__product_name', 'user__username')
admin.site.register(ProductReview, ProductReviewAdmin)
