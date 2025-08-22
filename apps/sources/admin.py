"""
Admin interface for Telegram sources.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    """Admin interface for Source model."""
    list_display = [
        'account', 
        'input_identifier', 
        'title', 
        'username', 
        'channel_id', 
        'is_private', 
        'is_active', 
        'mode', 
        'last_validation_status'
    ]
    list_filter = [
        'is_active', 
        'mode', 
        'is_private', 
        'last_validation_status', 
        'account'
    ]
    search_fields = ['input_identifier', 'title', 'username']
    ordering = ['-created_at']
    
    readonly_fields = [
        'channel_id', 
        'username', 
        'title', 
        'invite_link', 
        'is_private',
        'last_validated_at', 
        'last_validation_status', 
        'last_validation_error',
        'created_at', 
        'updated_at'
    ]
    
    fieldsets = (
        ('Source Configuration', {
            'fields': ('account', 'input_identifier', 'is_active', 'show_source', 'mode')
        }),
        ('Channel Information', {
            'fields': ('channel_id', 'username', 'title', 'invite_link', 'is_private'),
            'description': 'Channel information (populated after validation)'
        }),
        ('Validation', {
            'fields': ('last_validated_at', 'last_validation_status', 'last_validation_error'),
            'description': 'Validation status and error information'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['validate_sources', 'activate_sources', 'deactivate_sources']
    
    def validate_sources(self, request, queryset):
        """Validate selected sources."""
        for source in queryset:
            try:
                # This would integrate with Telethon to validate the source
                source.update_validation_status('ok')
                messages.success(
                    request, 
                    f"Source {source.input_identifier} validated successfully"
                )
            except Exception as e:
                source.update_validation_status('failed', str(e))
                messages.error(
                    request, 
                    f"Failed to validate {source.input_identifier}: {str(e)}"
                )
    
    validate_sources.short_description = "Validate selected sources"
    
    def activate_sources(self, request, queryset):
        """Activate selected sources."""
        count = queryset.update(is_active=True)
        messages.success(request, f"{count} sources activated")
    
    activate_sources.short_description = "Activate selected sources"
    
    def deactivate_sources(self, request, queryset):
        """Deactivate selected sources."""
        count = queryset.update(is_active=False)
        messages.success(request, f"{count} sources deactivated")
    
    deactivate_sources.short_description = "Deactivate selected sources"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('account')
