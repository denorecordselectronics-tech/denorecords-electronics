from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import Category, Product, HeroCarousel

@admin.register(Category)
class CategoryAdmin(UnfoldModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(UnfoldModelAdmin):
    list_display = ('name', 'category', 'original_price', 'price', 'is_available', 'order', 'created_at')
    list_editable = ('is_available', 'order')
    list_filter = ('category', 'is_available', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(HeroCarousel)
class HeroCarouselAdmin(UnfoldModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')
