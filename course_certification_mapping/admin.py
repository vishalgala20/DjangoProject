from django.contrib import admin
from .models import CourseCertificationMapping


@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at']
    list_filter = ['primary_mapping', 'is_active', 'created_at']
    search_fields = ['course__name', 'certification__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Mapping Information', {
            'fields': ('course', 'certification')
        }),
        ('Configuration', {
            'fields': ('primary_mapping', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
