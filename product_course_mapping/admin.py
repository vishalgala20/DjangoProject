from django.contrib import admin
from .models import ProductCourseMapping


@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'course', 'primary_mapping', 'is_active', 'created_at']
    list_filter = ['primary_mapping', 'is_active', 'created_at']
    search_fields = ['product__name', 'course__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Mapping Information', {
            'fields': ('product', 'course')
        }),
        ('Configuration', {
            'fields': ('primary_mapping', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
