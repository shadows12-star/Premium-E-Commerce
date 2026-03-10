from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'description')
    search_fields = ('category_name', 'slug')
    list_display_links = ('category_name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    prepopulated_fields = {'slug': ('category_name',)}
admin.site.register(Category, CategoryAdmin)