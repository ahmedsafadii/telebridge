"""
Core models for TeleBridge application.
"""

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating created_at and updated_at fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(TimeStampedModel):
    """
    Model to store country information for Telegram accounts.
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, help_text="ISO 3166-1 alpha-3 country code")
    phone_code = models.CharField(max_length=10, blank=True, help_text="International phone code")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class ValidationStatus(models.TextChoices):
    """
    Choices for validation status.
    """
    OK = 'ok', 'OK'
    FAILED = 'failed', 'Failed'
    UNKNOWN = 'unknown', 'Unknown'
    PENDING = 'pending', 'Pending'


class SessionStatus(models.TextChoices):
    """
    Choices for Telegram session status.
    """
    OK = 'ok', 'OK'
    FAILED = 'failed', 'Failed'
    UNKNOWN = 'unknown', 'Unknown'
    PENDING = 'pending', 'Pending'
    LOGGING_IN = 'logging_in', 'Logging In'
    NEED_CODE = 'need_code', 'Need Code'
    NEED_PASSWORD = 'need_password', 'Need Password'
