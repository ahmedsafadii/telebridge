"""
Celery tasks for Telegram account management.
"""

from celery import shared_task
from django.utils import timezone
from .models import TelegramAccount
from apps.core.models import SessionStatus


@shared_task
def check_account_status(account_id):
    """
    Check the status of a Telegram account.
    """
    try:
        account = TelegramAccount.objects.get(id=account_id)
        
        # This would integrate with Telethon to check account status
        # For now, we'll just update the timestamp
        account.last_check_at = timezone.now()
        account.save(update_fields=['last_check_at'])
        
        return f"Status checked for account {account.name}"
    except TelegramAccount.DoesNotExist:
        return f"Account with ID {account_id} not found"


@shared_task
def start_login_process(account_id):
    """
    Start the login process for a Telegram account.
    """
    try:
        account = TelegramAccount.objects.get(id=account_id)
        
        # This would integrate with Telethon to start login
        account.session_status = SessionStatus.LOGGING_IN
        account.save(update_fields=['session_status'])
        
        return f"Login process started for account {account.name}"
    except TelegramAccount.DoesNotExist:
        return f"Account with ID {account_id} not found"


@shared_task
def validate_all_accounts():
    """
    Validate all active Telegram accounts.
    """
    accounts = TelegramAccount.objects.filter(is_active=True)
    results = []
    
    for account in accounts:
        try:
            # This would integrate with Telethon to validate the account
            account.last_check_at = timezone.now()
            account.save(update_fields=['last_check_at'])
            results.append(f"Account {account.name} validated successfully")
        except Exception as e:
            account.update_session_status(SessionStatus.FAILED, str(e))
            results.append(f"Account {account.name} validation failed: {str(e)}")
    
    return results


@shared_task
def cleanup_inactive_sessions():
    """
    Clean up inactive sessions and update status.
    """
    # This task would check for stale sessions and update their status
    # Implementation would depend on Telethon integration
    return "Session cleanup completed"
