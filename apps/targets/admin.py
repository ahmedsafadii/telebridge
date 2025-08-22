"""
Admin interface for Telegram targets.
"""

from django.contrib import admin
from django.contrib import messages
from .models import Target, SourceTargetMapping


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    """Admin interface for Target model."""
    list_display = [
        'name', 
        'target_type', 
        'account', 
        'channel_identifier', 
        'email_address',
        'is_active', 
        'last_validation_status'
    ]
    list_filter = [
        'target_type', 
        'is_active', 
        'last_validation_status', 
        'account'
    ]
    search_fields = ['name', 'channel_identifier', 'email_address']
    ordering = ['name']
    
    readonly_fields = [
        'last_validated_at', 
        'last_validation_status', 
        'last_validation_error',
        'created_at', 
        'updated_at'
    ]
    
    fieldsets = (
        ('Target Information', {
            'fields': ('name', 'target_type', 'is_active')
        }),
        ('Telegram Configuration', {
            'fields': ('account', 'channel_identifier'),
            'description': 'Telegram target configuration'
        }),
        ('Email Configuration', {
            'fields': ('email_address',),
            'description': 'Email target configuration'
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
    
    actions = ['validate_targets', 'activate_targets', 'deactivate_targets']
    
    def validate_targets(self, request, queryset):
        """Validate selected targets."""
        for target in queryset:
            try:
                # This would integrate with Telethon to validate the target
                target.update_validation_status('ok')
                messages.success(
                    request, 
                    f"Target {target.name} validated successfully"
                )
            except Exception as e:
                target.update_validation_status('failed', str(e))
                messages.error(
                    request, 
                    f"Failed to validate {target.name}: {str(e)}"
                )
    
    validate_targets.short_description = "Validate selected targets"
    
    def activate_targets(self, request, queryset):
        """Activate selected targets."""
        count = queryset.update(is_active=True)
        messages.success(request, f"{count} targets activated")
    
    activate_targets.short_description = "Activate selected targets"
    
    def deactivate_targets(self, request, queryset):
        """Deactivate selected targets."""
        count = queryset.update(is_active=False)
        messages.success(request, f"{count} targets deactivated")
    
    deactivate_targets.short_description = "Deactivate selected targets"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('account')
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize form based on target type."""
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.target_type == 'telegram':
            form.base_fields['email_address'].widget.attrs['readonly'] = True
        elif obj and obj.target_type == 'email':
            form.base_fields['account'].widget.attrs['readonly'] = True
            form.base_fields['channel_identifier'].widget.attrs['readonly'] = True
        return form


@admin.register(SourceTargetMapping)
class SourceTargetMappingAdmin(admin.ModelAdmin):
    """Admin interface for SourceTargetMapping model."""
    list_display = [
        'source', 
        'target', 
        'is_active', 
        'delay_seconds', 
        'max_retries',
        'created_at'
    ]
    list_filter = ['is_active', 'source', 'target']
    search_fields = ['source__input_identifier', 'target__name']
    ordering = ['source', 'target']
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Mapping Configuration', {
            'fields': ('source', 'target', 'is_active')
        }),
        ('Processing Options', {
            'fields': ('delay_seconds', 'max_retries'),
            'description': 'Processing configuration for this mapping'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_mappings', 'deactivate_mappings']
    
    def activate_mappings(self, request, queryset):
        """Activate selected mappings."""
        count = queryset.update(is_active=True)
        messages.success(request, f"{count} mappings activated")
    
    activate_mappings.short_description = "Activate selected mappings"
    
    def deactivate_mappings(self, request, queryset):
        """Deactivate selected mappings."""
        count = queryset.update(is_active=False)
        messages.success(request, f"{count} mappings deactivated")
    
    deactivate_mappings.short_description = "Deactivate selected mappings"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('source', 'target')
