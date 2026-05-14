from django.contrib import admin
from .models import ProductReview, Products,Variations,ProductGallery
# Register your models here.
import admin_thumbnails
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1 
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available', 'created_date', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name',)
    list_display_links = ('product_name',)
    filter_horizontal = ()
    inlines = [ProductGalleryInline]
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
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__product_name',)
admin.site.register(ProductGallery, ProductGalleryAdmin)