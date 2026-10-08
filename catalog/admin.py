from django.contrib import admin
from catalog.models import Product, Category, ContactRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_published', 'owner', 'created_at')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('name', 'description')
    list_display_links = ('id', 'name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'phone', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)