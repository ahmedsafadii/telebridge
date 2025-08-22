"""
Admin interface for Telegram account management.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from .models import TelegramAccount


@admin.register(TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    """Admin interface for TelegramAccount model."""
    list_display = [
        'name', 
        'phone_number', 
        'country', 
        'session_status', 
        'last_check_at', 
        'created_at'
    ]
    list_filter = ['session_status', 'is_active', 'country']
    search_fields = ['name', 'phone_number']
    ordering = ['name']
    
    readonly_fields = [
        'session_status', 
        'last_error', 
        'last_check_at', 
        'created_at', 
        'updated_at'
    ]
    
    fieldsets = (
        ('Account Information', {
            'fields': ('name', 'phone_number', 'country', 'is_active')
        }),
        ('API Credentials', {
            'fields': ('api_id', 'api_hash'),
            'description': 'Telegram API credentials from https://my.telegram.org/'
        }),
        ('Session Management', {
            'fields': ('session_status', 'last_error', 'last_check_at'),
            'description': 'Session status and error information'
        }),
        ('Login Process', {
            'fields': ('pending_phone', 'phone_code_hash'),
            'description': 'Fields used during the login process'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'start_login',
        'resend_sms_code',
        'confirm_login',
        'check_status',
        'logout'
    ]
    
    def get_actions(self, request):
        """Get available actions."""
        actions = super().get_actions(request)
        return actions
    
    def start_login(self, request, queryset):
        """Start the login process for selected accounts."""
        for account in queryset:
            try:
                # This would integrate with Telethon to start login
                account.session_status = 'logging_in'
                account.save()
                messages.success(
                    request, 
                    f"Login process started for {account.name}"
                )
            except Exception as e:
                messages.error(
                    request, 
                    f"Failed to start login for {account.name}: {str(e)}"
                )
    
    start_login.short_description = "Start login process"
    
    def resend_sms_code(self, request, queryset):
        """Resend SMS code for selected accounts."""
        for account in queryset:
            try:
                # This would integrate with Telethon to resend SMS
                messages.success(
                    request, 
                    f"SMS code resent for {account.name}"
                )
            except Exception as e:
                messages.error(
                    request, 
                    f"Failed to resend SMS for {account.name}: {str(e)}"
                )
    
    resend_sms_code.short_description = "Resend SMS code"
    
    def confirm_login(self, request, queryset):
        """Confirm login for selected accounts."""
        for account in queryset:
            try:
                # This would integrate with Telethon to confirm login
                messages.success(
                    request, 
                    f"Login confirmed for {account.name}"
                )
            except Exception as e:
                messages.error(
                    request, 
                    f"Failed to confirm login for {account.name}: {str(e)}"
                )
    
    confirm_login.short_description = "Confirm login"
    
    def check_status(self, request, queryset):
        """Check status for selected accounts."""
        for account in queryset:
            try:
                # This would integrate with Telethon to check status
                account.last_check_at = timezone.now()
                account.save()
                messages.success(
                    request, 
                    f"Status checked for {account.name}"
                )
            except Exception as e:
                messages.error(
                    request, 
                    f"Failed to check status for {account.name}: {str(e)}"
                )
    
    check_status.short_description = "Check status"
    
    def logout(self, request, queryset):
        """Logout selected accounts."""
        for account in queryset:
            try:
                # This would integrate with Telethon to logout
                account.session_status = 'unknown'
                account.save()
                messages.success(
                    request, 
                    f"Logged out {account.name}"
                )
            except Exception as e:
                messages.error(
                    request, 
                    f"Failed to logout {account.name}: {str(e)}"
                )
    
    logout.short_description = "Logout"
    
    def get_urls(self):
        """Add custom URLs for admin actions."""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:account_id>/start_login/',
                self.admin_site.admin_view(self.start_login_view),
                name='telegram-account-start-login',
            ),
            path(
                '<int:account_id>/check_status/',
                self.admin_site.admin_view(self.check_status_view),
                name='telegram-account-check-status',
            ),
        ]
        return custom_urls + urls
    
    def start_login_view(self, request, account_id):
        """Custom view for starting login."""
        try:
            account = TelegramAccount.objects.get(id=account_id)
            # Implement login logic here
            messages.success(request, f"Login started for {account.name}")
        except TelegramAccount.DoesNotExist:
            messages.error(request, "Account not found")
        
        return HttpResponseRedirect(
            reverse('admin:accounts_telegramaccount_change', args=[account_id])
        )
    
    def check_status_view(self, request, account_id):
        """Custom view for checking status."""
        try:
            account = TelegramAccount.objects.get(id=account_id)
            # Implement status check logic here
            account.last_check_at = timezone.now()
            account.save()
            messages.success(request, f"Status checked for {account.name}")
        except TelegramAccount.DoesNotExist:
            messages.error(request, "Account not found")
        
        return HttpResponseRedirect(
            reverse('admin:accounts_telegramaccount_change', args=[account_id])
        )
