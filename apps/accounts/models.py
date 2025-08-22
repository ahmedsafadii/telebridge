"""
Models for Telegram account management.
"""

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel, Country, SessionStatus
from django.utils import timezone


class TelegramAccount(TimeStampedModel):
    """
    Model to store Telegram account information and manage sessions.
    """
    name = models.CharField(
        max_length=100, 
        help_text="Friendly label for this account"
    )
    api_id = models.CharField(max_length=50)
    api_hash = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    country = models.ForeignKey(
        Country, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    is_active = models.BooleanField(default=True)
    
    # Session management
    session_status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.UNKNOWN,
        help_text="Last known session status: ok/failed/unknown"
    )
    last_error = models.TextField(blank=True, help_text="Last error message")
    
    # Login process fields
    pending_phone = models.CharField(max_length=20, blank=True)
    phone_code_hash = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    last_check_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Telegram Account"
        verbose_name_plural = "Telegram Accounts"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    def get_display_name(self):
        """Return display name with phone number."""
        return f"{self.name} (+{self.phone_number})"

    def update_session_status(self, status, error_message=""):
        """Update session status and error message."""
        self.session_status = status
        if error_message:
            self.last_error = error_message
        self.last_check_at = timezone.now()
        self.save(update_fields=['session_status', 'last_error', 'last_check_at'])

    def is_session_valid(self):
        """Check if the session is valid."""
        return self.session_status == SessionStatus.OK
