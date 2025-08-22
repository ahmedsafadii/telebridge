"""
Admin interface for Telegram account management.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from django import forms
from django.shortcuts import render
from .models import TelegramAccount
from .services import TelegramClientService, run_async


class PhoneCodeForm(forms.Form):
    """Form for entering phone code."""
    phone_code = forms.CharField(
        max_length=6,
        min_length=6,
        label="Phone Code",
        help_text="Enter the 6-digit code sent to your Telegram"
    )


class PasswordForm(forms.Form):
    """Form for entering 2FA password."""
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Two-Factor Password",
        help_text="Enter your Telegram two-factor authentication password"
    )


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
                service = TelegramClientService(account)
                success, message = run_async(service.start_login_process())
                
                if success:
                    messages.success(request, f"Login process started for {account.name}: {message}")
                else:
                    messages.error(request, f"Failed to start login for {account.name}: {message}")
                    
            except Exception as e:
                messages.error(request, f"Failed to start login for {account.name}: {str(e)}")
    
    start_login.short_description = "Start login process"
    
    def resend_sms_code(self, request, queryset):
        """Resend SMS code for selected accounts."""
        for account in queryset:
            try:
                service = TelegramClientService(account)
                success, message = run_async(service.start_login_process())
                
                if success:
                    messages.success(request, f"SMS code resent for {account.name}: {message}")
                else:
                    messages.error(request, f"Failed to resend SMS for {account.name}: {message}")
                    
            except Exception as e:
                messages.error(request, f"Failed to resend SMS for {account.name}: {str(e)}")
    
    resend_sms_code.short_description = "Resend SMS code"
    
    def confirm_login(self, request, queryset):
        """Confirm login for selected accounts."""
        if len(queryset) != 1:
            messages.error(request, "Please select exactly one account to confirm login")
            return
        
        account = queryset.first()
        
        # Check if we need to show phone code form
        if account.session_status == 'phone_code_sent':
            return self.phone_code_form_view(request, account)
        elif account.session_status == 'password_needed':
            return self.password_form_view(request, account)
        else:
            messages.error(request, f"Account {account.name} is not in the correct state for login confirmation")
    
    confirm_login.short_description = "Confirm login"
    
    def check_status(self, request, queryset):
        """Check status for selected accounts."""
        for account in queryset:
            try:
                service = TelegramClientService(account)
                success, message = run_async(service.check_status())
                
                if success:
                    messages.success(request, f"Status checked for {account.name}: {message}")
                else:
                    messages.error(request, f"Failed to check status for {account.name}: {message}")
                    
            except Exception as e:
                messages.error(request, f"Failed to check status for {account.name}: {str(e)}")
    
    check_status.short_description = "Check status"
    
    def logout(self, request, queryset):
        """Logout selected accounts."""
        for account in queryset:
            try:
                service = TelegramClientService(account)
                success, message = run_async(service.logout())
                
                if success:
                    messages.success(request, f"Logged out {account.name}: {message}")
                else:
                    messages.error(request, f"Failed to logout {account.name}: {message}")
                    
            except Exception as e:
                messages.error(request, f"Failed to logout {account.name}: {str(e)}")
    
    logout.short_description = "Logout"
    
    def phone_code_form_view(self, request, account):
        """Show phone code form."""
        if request.method == 'POST':
            form = PhoneCodeForm(request.POST)
            if form.is_valid():
                phone_code = form.cleaned_data['phone_code']
                try:
                    service = TelegramClientService(account)
                    success, message = run_async(service.confirm_phone_code(phone_code))
                    
                    if success:
                        messages.success(request, f"Login successful for {account.name}: {message}")
                    else:
                        messages.error(request, f"Login failed for {account.name}: {message}")
                        
                    return HttpResponseRedirect(
                        reverse('admin:accounts_telegramaccount_change', args=[account.id])
                    )
                except Exception as e:
                    messages.error(request, f"Error confirming code: {str(e)}")
        else:
            form = PhoneCodeForm()
        
        context = {
            'title': f'Enter Phone Code for {account.name}',
            'form': form,
            'account': account,
            'opts': self.model._meta,
        }
        return render(request, 'admin/accounts/telegramaccount/phone_code_form.html', context)
    
    def password_form_view(self, request, account):
        """Show password form for 2FA."""
        if request.method == 'POST':
            form = PasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                try:
                    service = TelegramClientService(account)
                    success, message = run_async(service.confirm_password(password))
                    
                    if success:
                        messages.success(request, f"Two-factor authentication successful for {account.name}: {message}")
                    else:
                        messages.error(request, f"Two-factor authentication failed for {account.name}: {message}")
                        
                    return HttpResponseRedirect(
                        reverse('admin:accounts_telegramaccount_change', args=[account.id])
                    )
                except Exception as e:
                    messages.error(request, f"Error confirming password: {str(e)}")
        else:
            form = PasswordForm()
        
        context = {
            'title': f'Enter Two-Factor Password for {account.name}',
            'form': form,
            'account': account,
            'opts': self.model._meta,
        }
        return render(request, 'admin/accounts/telegramaccount/password_form.html', context)
    
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
            service = TelegramClientService(account)
            success, message = run_async(service.start_login_process())
            
            if success:
                messages.success(request, f"Login started for {account.name}: {message}")
            else:
                messages.error(request, f"Failed to start login for {account.name}: {message}")
                
        except TelegramAccount.DoesNotExist:
            messages.error(request, "Account not found")
        
        return HttpResponseRedirect(
            reverse('admin:accounts_telegramaccount_change', args=[account_id])
        )
    
    def check_status_view(self, request, account_id):
        """Custom view for checking status."""
        try:
            account = TelegramAccount.objects.get(id=account_id)
            service = TelegramClientService(account)
            success, message = run_async(service.check_status())
            
            if success:
                messages.success(request, f"Status checked for {account.name}: {message}")
            else:
                messages.error(request, f"Failed to check status for {account.name}: {message}")
                
        except TelegramAccount.DoesNotExist:
            messages.error(request, "Account not found")
        
        return HttpResponseRedirect(
            reverse('admin:accounts_telegramaccount_change', args=[account_id])
        )
