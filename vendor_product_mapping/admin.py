from django.contrib import admin
from .models import VendorProductMapping


@admin.register(VendorProductMapping)
class VendorProductMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'product', 'primary_mapping', 'is_active', 'created_at']
    list_filter = ['primary_mapping', 'is_active', 'created_at']
    search_fields = ['vendor__name', 'product__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Mapping Information', {
            'fields': ('vendor', 'product')
        }),
        ('Configuration', {
            'fields': ('primary_mapping', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
