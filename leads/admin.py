from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(UnfoldModelAdmin):
    list_display = ('product_name', 'customer_phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product_name', 'customer_phone', 'message')
    readonly_fields = ('created_at',)
