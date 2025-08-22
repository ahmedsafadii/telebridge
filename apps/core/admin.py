"""
Admin interface for core models.
"""

from django.contrib import admin
from .models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin interface for Country model."""
    list_display = ['name', 'code', 'phone_code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'phone_code')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
